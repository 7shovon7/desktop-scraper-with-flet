import os
from time import sleep
import flet as ft
from script import scrape


SELECTED_FILE = None
SCRAPING = False


def main(page: ft.Page):

    def choose_file_path(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            global SELECTED_FILE
            SELECTED_FILE = e.files[0].path
            selected_files.value = f"Selected file:\n{SELECTED_FILE}"
            selected_files.update()

    def update_progress_bar(percentage):
        pb.value = percentage * 0.01
        pb.update()

    def update_list_messages(msg):
        list_view.controls.append(ft.Text(msg))
        list_view.update()

    def change_scraping_status(status=None):
        if status is not None:
            global SCRAPING
            SCRAPING = status
        return SCRAPING

    def start_scraping(e, view: ft.Column):
        if SELECTED_FILE:
            global SCRAPING
            SCRAPING = True
            scraping_text = ft.Text('Scraping...')
            view.controls += [
                ft.Row(
                    controls=[
                        scraping_text,
                        ft.IconButton(
                            icon=ft.icons.CANCEL,
                            on_click=lambda _: change_scraping_status(False)
                        )
                    ]
                ),
                pb,
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                ft.Container(
                    content=list_view,
                    expand=True,
                ),
            ]
            view.update()
            scrape(
                SELECTED_FILE,
                os.path.split(SELECTED_FILE)[0],
                progress_callback=update_progress_bar,
                progress_msg_callback=update_list_messages,
                test=False,
                scraping_status=change_scraping_status,
            )
            scraping_text.value = 'Scraping completed!'
            scraping_text.update()
        else:
            print('no file chosen')

    pick_files_dialog = ft.FilePicker(on_result=choose_file_path)
    selected_files = ft.Text("Selected file:\n/User/mars/Downloads/comparison.xlsx")
    pb = ft.ProgressBar(value=0)
    list_view = ft.ListView(
        controls=[],
        auto_scroll=True,
    )

    view = ft.Column(
        expand=True,
        width=600,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Text("Select input sheet"),
            ft.CupertinoFilledButton(
                text='Choose...',
                opacity_on_click=0.3,
                on_click=pick_files_dialog.pick_files,
            ),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            selected_files,
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
            ft.CupertinoFilledButton(
                text="Start Collecting Data",
                opacity_on_click=0.3,
                on_click=lambda _: start_scraping(_, view),
            ),
            ft.Divider(height=20, color=ft.colors.TRANSPARENT),
        ],
    )
    
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.overlay.append(pick_files_dialog)
    page.add(view)

ft.app(target=main)
