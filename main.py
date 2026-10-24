from gc import disable

import flet as ft
from flet import IconButton
from flet.controls import alignment

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    tipo = ft.TextField("Tipo")
    marca = ft.TextField("Marca")
    anno = ft.TextField("Anno acquisto")

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def aggiungi_handler(e):
        try:
            anno_int = int(anno.value)
        except ValueError:
            alert.show_alert("Errore: inserisci un valore numerico valido per l'anno.")
            return

        valore_float = float(myText.value)

        # Aggiunge lo strumento alla struttura dati
        deposito.aggiungi_strumento(tipo.value, marca.value, anno_int, valore_float)

        # Svuota i campi e resetta il contatore
        tipo.value = ""
        marca.value = ""
        anno.value = ""
        myText.value = "0"
        aggiorna_lista_strumenti()
        page.update()
    def handler_minus(e):
        v = int(myText.value)
        v -= 1
        myText.value = v
        myText.update()

    def handler_plus(e):
        v = int(myText.value)
        v += 1
        myText.value = v
        myText.update()


    bottoneMeno = ft.IconButton(icon=ft.Icons.REMOVE, icon_color=ft.Colors.RED, on_click=handler_minus)
    bottonePiu = ft.IconButton(icon=ft.Icons.ADD, icon_color=ft.Colors.GREEN, on_click=handler_plus)
    myText = ft.TextField(value=0, disabled=True, width = 60, text_align=ft.TextAlign.CENTER)

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    list_view = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)
    testoStrumento = ft.Text("Aggiungi nuovo strumento:", size = 20)
    count = 1
    strumenti = deposito.strumenti_ordinati_per_marca()
    for strumento in strumenti:
        if strumento.disponibile:
            stato = "Disponibile"
        else:
            stato = "In prestito"
    for i in range(0, 60):
        list_view.controls.append(ft.Text(f"{count}) {strumento.marca} - {strumento.tipo} - {strumento.anno_acquisto} -  Stato: {stato}"))
        count += 1

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        testoStrumento,
        ft.Row([tipo, marca,anno,bottoneMeno, myText, bottonePiu], alignment=ft.MainAxisAlignment.CENTER),
        ft.Button("Aggiungi Strumento", on_click=aggiungi_handler),
        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti
    )
    aggiorna_lista_strumenti()

ft.run(main)
