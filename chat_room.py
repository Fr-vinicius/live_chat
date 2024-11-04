import flet as ft


def main(page):

    img = ft.Image(
        src=f"https://cauterfixrestrict.nyc3.cdn.digitaloceanspaces.com/public/chat_img.png",
        width=150,
        height=150,
        fit=ft.ImageFit.CONTAIN,
    )

    page.title = "Chat Dev"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.add(img)
    page.update()

    initial_title = ft.Text('Bem vindo ao chat Dev!',
    size=20, weight="bold",
    color=ft.colors.BLUE_500)
    
    user_name_input = ft.TextField(label='Nome', width=300)
    messages_field = ft.Column()


    def send_message_to_all(info):

        messages_field.controls.append(ft.Text(info))
        page.update()

    page.pubsub.subscribe(send_message_to_all)


    def send_message(event):

        message_content = f"{user_name_input.value} disse: {message_input.value}"
        page.pubsub.send_all(message_content)
        message_input.value = ''
        page.update()

    
    def leave_chat_room(event):

        page.remove(actions_container, messages_field)
        left_chat_notification = f"{user_name_input.value} saiu do chat."
        page.pubsub.send_all(left_chat_notification)
        page.add(img)
        page.add(initial_title)
        page.add(start_chat_button)
        user_name_input.value=''
        page.update()
    
    message_input = ft.TextField(label='Digite sua mensagem',
    width=500, on_submit=send_message)

    send_message_button = ft.ElevatedButton('Enviar',
    bgcolor=ft.colors.LIGHT_BLUE,
    on_click=send_message)

    leave_chat_button = ft.ElevatedButton(text="Sair",
    on_click=leave_chat_room,
    bgcolor=ft.colors.YELLOW_200)

    actions_container = ft.Row([message_input,
    send_message_button,
    leave_chat_button ],
    alignment="center")


    def enter_chat_room(event):

        join_chat_modal.open = False
        page.remove(start_chat_button)
        page.remove(initial_title)
        page.remove(img)
        page.add(messages_field, actions_container)

        joined_chat_notification = f"{user_name_input.value} acabou de entrar no chat."

        page.pubsub.send_all(joined_chat_notification)
        message_input.focus()
        page.update()

    join_chat_button = ft.ElevatedButton('Entrar', on_click=enter_chat_room)

    join_chat_modal = ft.AlertDialog(
    open=False,
    modal=True,
    title=ft.Text('Digite seu nome para iniciar'),
    content=user_name_input,
    actions=[join_chat_button]
    )


    def start_chat(event):

        page.dialog = join_chat_modal
        join_chat_modal.open = True
        page.update()

    start_chat_button = ft.ElevatedButton('Iniciar chat', on_click=start_chat)

    page.add(initial_title, start_chat_button)


if __name__ == "__main__":
    ft.app(main, view=ft.WEB_BROWSER, port=8000)
