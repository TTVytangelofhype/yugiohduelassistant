"""Manual post-duel adviser; never interfaces with the running game."""
import base64
import io
import json
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
from engine import read_deck, deck_statistics, battle_damage, checklist

class App:
    def __init__(self, root):
        self.root = root
        root.title("NEXUS Duel AI — All Decks")
        root.geometry("1000x780")
        self.deck = {"name":"My Deck","main":{},"extra":{},"side":{}}
        self.image_bytes = None
        self.model = tk.StringVar(value="gemma3:4b")
        self.phase = tk.StringVar(value="Main Phase 1")
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        board = ttk.Frame(notebook, padding=10)
        notebook.add(board, text="Board Study")
        for row,(name,attr) in enumerate((("Your hand","hand"),("Your field","field"),("Your graveyard","grave"),("Available extra-deck cards","extra"),("Opponent board/revealed cards","opp"))):
            ttk.Label(board,text=name).grid(row=row,column=0,sticky="nw",pady=4)
            area=tk.Text(board,height=3,width=85)
            area.grid(row=row,column=1,sticky="ew",pady=4)
            setattr(self,attr,area)
        board.columnconfigure(1,weight=1)
        tools=ttk.Frame(board)
        tools.grid(row=5,column=0,columnspan=2,sticky="ew",pady=8)
        ttk.Label(tools,text="Phase").pack(side="left")
        ttk.Combobox(tools,textvariable=self.phase,values=["Draw","Standby","Main Phase 1","Battle","Main Phase 2","End"],width=16,state="readonly").pack(side="left",padx=6)
        ttk.Button(tools,text="Load Screenshot",command=self.load_image).pack(side="left",padx=4)
        ttk.Button(tools,text="Paste Screenshot",command=self.paste_image).pack(side="left",padx=4)
        ttk.Button(tools,text="Offline Checklist",command=self.offline).pack(side="left",padx=4)
        ai=ttk.Frame(board)
        ai.grid(row=6,column=0,columnspan=2,sticky="ew",pady=8)
        ttk.Label(ai,text="Ollama model:").pack(side="left")
        ttk.Entry(ai,textvariable=self.model,width=20).pack(side="left",padx=6)
        ttk.Button(ai,text="Local AI Analysis",command=self.start_ai).pack(side="left")
        self.image_label=ttk.Label(ai,text="No screenshot chosen")
        self.image_label.pack(side="left",padx=10)
        self.output=tk.Text(board,height=15,wrap="word")
        self.output.grid(row=7,column=0,columnspan=2,sticky="nsew")
        board.rowconfigure(7,weight=1)
        d=ttk.Frame(notebook,padding=12)
        notebook.add(d,text="Deck Manager")
        self.deck_name=tk.StringVar(value=self.deck["name"])
        ttk.Label(d,text="Deck name").pack(anchor="w")
        ttk.Entry(d,textvariable=self.deck_name,width=50).pack(anchor="w")
        ttk.Label(d,text="One card per line: Card Name | quantity (1 to 3). Use tab for each deck zone.").pack(anchor="w",pady=10)
        self.deck_zones={}
        tabs=ttk.Notebook(d)
        tabs.pack(fill="both",expand=True)
        for zone in ("main","extra","side"):
            frame=ttk.Frame(tabs)
            tabs.add(frame,text=zone.title())
            area=tk.Text(frame)
            area.pack(fill="both",expand=True)
            self.deck_zones[zone]=area
        actions=ttk.Frame(d)
        actions.pack(fill="x",pady=8)
        ttk.Button(actions,text="Import JSON",command=self.import_deck).pack(side="left",padx=4)
        ttk.Button(actions,text="Export JSON",command=self.export_deck).pack(side="left",padx=4)
        ttk.Button(actions,text="Check Counts",command=self.check_deck).pack(side="left",padx=4)
        damage=ttk.Frame(notebook,padding=15)
        notebook.add(damage,text="Damage Calculator")
        self.atk=tk.StringVar(value="3000")
        self.defense=tk.StringVar(value="2500")
        self.position=tk.StringVar(value="Attack")
        self.direct=tk.BooleanVar(value=False)
        for label,variable in (("Your monster ATK",self.atk),("Opposing ATK or DEF",self.defense)):
            ttk.Label(damage,text=label).pack(anchor="w")
            ttk.Entry(damage,textvariable=variable).pack(anchor="w",pady=5)
        ttk.Combobox(damage,textvariable=self.position,values=["Attack","Defense"],state="readonly").pack(anchor="w")
        ttk.Checkbutton(damage,text="Direct attack",variable=self.direct).pack(anchor="w",pady=8)
        ttk.Button(damage,text="Calculate",command=self.calc).pack(anchor="w")
        self.result=ttk.Label(damage,text="")
        self.result.pack(anchor="w",pady=10)

    def area(self,key):
        return getattr(self,key).get("1.0","end").strip()
    def write(self,text):
        self.output.delete("1.0","end")
        self.output.insert("end",text)
    def load_image(self):
        path=filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg *.webp")])
        if path:
            self.image_bytes=Path(path).read_bytes()
            self.image_label.config(text=Path(path).name)
    def paste_image(self):
        try:
            from PIL import ImageGrab
            clip=ImageGrab.grabclipboard()
            if hasattr(clip,"save"):
                b=io.BytesIO()
                clip.convert("RGB").save(b,format="PNG")
                self.image_bytes=b.getvalue()
                self.image_label.config(text="Clipboard image loaded")
                return
            messagebox.showwarning("Clipboard","Copy a screenshot (Win+Shift+S) and try again.")
        except Exception as exc:
            messagebox.showerror("Clipboard",str(exc))
    def offline(self):
        self.write(checklist(*(self.area(x) for x in ("hand","field","grave","extra","opp")),self.phase.get(),self.deck))
    def parse_deck(self):
        deck={"name":self.deck_name.get().strip() or "Unnamed Deck"}
        for zone,area in self.deck_zones.items():
            cards={}
            for line in area.get("1.0","end").splitlines():
                if not line.strip(): continue
                pieces=line.rsplit("|",1)
                name=pieces[0].strip()
                count=int(pieces[1].strip()) if len(pieces)>1 else 1
                if not name or not 0<=count<=3: raise ValueError("Invalid card/count: "+line)
                cards[name]=count
            deck[zone]=cards
        self.deck=deck
        return deck
    def fill_deck(self,deck):
        self.deck=deck
        self.deck_name.set(deck.get("name","My Deck"))
        for zone,area in self.deck_zones.items():
            area.delete("1.0","end")
            area.insert("1.0","\n".join(f"{name} | {n}" for name,n in deck.get(zone,{}).items()))
    def import_deck(self):
        path=filedialog.askopenfilename(filetypes=[("Deck JSON","*.json")])
        if path:
            try: self.fill_deck(read_deck(path))
            except Exception as exc: messagebox.showerror("Invalid deck",str(exc))
    def export_deck(self):
        try:
            deck=self.parse_deck()
            path=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("Deck JSON","*.json")])
            if path: Path(path).write_text(json.dumps(deck,indent=2),encoding="utf-8")
        except Exception as exc: messagebox.showerror("Invalid deck",str(exc))
    def check_deck(self):
        try: messagebox.showinfo("Deck counts",json.dumps(deck_statistics(self.parse_deck()),indent=2)+"\nThese counts are NOT a legality/banlist check.")
        except Exception as exc: messagebox.showerror("Invalid deck",str(exc))
    def calc(self):
        try:
            r=battle_damage(int(self.atk.get()),int(self.defense.get()),self.position.get(),self.direct.get())
            self.result.config(text=f"Damage to opponent: {r['opponent']} | Damage to you: {r['you']}")
        except Exception as exc: messagebox.showerror("Input error",str(exc))
    def start_ai(self):
        if not self.image_bytes:
            messagebox.showinfo("Screenshot required","Select or paste a screenshot first.")
            return
        if not self.model.get().strip():
            messagebox.showerror("Model required","Enter an Ollama vision model name.")
            return
        self.write("Analysing locally via Ollama...")
        context={k:self.area(k) for k in ("hand","field","grave","extra","opp")}
        context["phase"]=self.phase.get()
        context["deck"]=self.deck
        image=self.image_bytes
        model=self.model.get().strip()
        threading.Thread(target=self.analyze_worker,args=(image,model,context),daemon=True).start()
    def analyze_worker(self,image,model,context):
        prompt=("Study this Yu-Gi-Oh! Master Duel screenshot for post-duel education only. "
                "Use only visible and provided cards. Never assume unrevealed cards. "
                "Describe recognized cards and uncertainty, candidate legal lines to VERIFY, "
                "damage considerations and likely interactions. Do not promise a win. "
                "The assistant is not an authoritative effect database. Context: "+json.dumps(context))
        payload={"model":model,"stream":False,"messages":[{"role":"user","content":prompt,"images":[base64.b64encode(image).decode("ascii")]}]}
        try:
            req=Request("http://127.0.0.1:11434/api/chat",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"},method="POST")
            with urlopen(req,timeout=240) as response: result=json.load(response)
            answer=result.get("message",{}).get("content","No model response.")
        except (URLError,TimeoutError,ValueError) as exc:
            answer="Ollama error: "+str(exc)+"\nInstall Ollama, pull a compatible vision model, and ensure it is running."
        except Exception as exc:
            answer="Local AI error: "+str(exc)
        self.root.after(0,lambda: self.write(answer))

if __name__=="__main__":
    root=tk.Tk()
    App(root)
    root.mainloop()
