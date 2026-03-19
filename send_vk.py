import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll


class MessageVk:

    def __init__(self, vk_token):

        if not vk_token:
            self.vk = False
        else:
            # Авторизация в VK API
            self.vk_session = vk_api.VkApi(token=vk_token)
            self.vk = self.vk_session.get_api()
            # Создаём объект для работы с событиями
            self.longpoll = VkLongPoll(self.vk_session)

    # Функция для отправки сообщений
    def send_message(self, peer_id, message):
        if not self.vk:
            return "VK is turn off."
        try:
            response = self.vk.messages.send(
                peer_id=peer_id, message=message, random_id=0
            )
            return response
        except Exception as e:
            print(f"Error send massage to VK: {e}")
            return e

    def test(self, vk_id):
        if not self.vk:
            return "VK is turn off."
        # Посылаем сообщение пользователю с указанным ID
        self.send_message(vk_id, message="Test1")


# # Запуск бота
# if __name__ == "__main__":
#     server1 = MessageVk(vk_token)
#     # server1.test()
#     massage = "Test5"
#     server1.send_message(vk_id_d, massage)
