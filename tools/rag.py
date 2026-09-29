import requests
def rag(ques: str):

    url = "http://localhost:8000/ask"

    try:

        response = requests.post(
            url,
            json={
                "question": ques
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data["answer"]

    except Exception as e:

        return {"ERROR --  Rag API Not Running-Go to the Folder and run the API = " 
                " /home/ubuntu/Desktop/DailyWork/Agent/RAG/Model1 = "
                "uvicorn main_api:app --host 0.0.0.0 --port 8000"}
    