import requests

class FCMService:
    
    def notify_user(self, user_id, title, message, data= {}):
        try:
            data = {
                "to": f"{user_id}",
                "sound": "default",
                "title": title,
                "body": message,
                "data": data
            }
            response = requests.post('https://exp.host/--/api/v2/push/send', json=data)
            if response.status_code != 200:
                print(f"Erro ao enviar notificação para usuário {user_id}: {response.json()}")
                raise ValueError("Erro ao enviar notificação")
            print(f"Usuário {user_id} notificado com sucesso")
            return response.json()
        except Exception as e:
            print(f"Erro ao enviar notificação para usuário {user_id}: {str(e)}")
            raise e
