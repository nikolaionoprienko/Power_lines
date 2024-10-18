import flet as ft


def main(page: ft.Page):  # свойства страницы
    page.title = "Тестим flet"
    page.theme_mode = "Dark"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    user_label = ft.Text('бади воз толд ми', color="#aa4926")
    user_text = ft.TextField(value='Пиши, заебал', width=450, text_align=ft.TextAlign.CENTER)

    def get_info(e):
        user_label.value = user_text.value
        page.update()

    page.add(  # Элементы будут расположены в одной строке
        ft.Row(
            [
                ft.IconButton(ft.icons.BOY, on_click=get_info),
                ft.Icon(ft.icons.BACKUP_SHARP),
                ft.ElevatedButton(text="Жми, Заебал", on_click=get_info),
                ft.OutlinedButton(text="Жми, Заебал, но в другом стиле", on_click=get_info),
                ft.Checkbox(label='Вы за поправки в Конституцию?', value=True, on_change=None)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    page.add(  # Ещё одна строка
        ft.Row(
            [
                ft.Text('Cам', color='#aa4926'),
                user_label,
                user_text
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )


ft.app(target=main)  # Запускает функцию, которая будет открываться при открытии приложения
                     # , view=ft.AppView.WEB_BROWSER: браузерное приложение

