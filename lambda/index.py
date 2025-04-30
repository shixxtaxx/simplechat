import json
import urllib.request

MODEL_ID = "https://a67d-35-247-77-171.ngrok-free.app"  # FastAPIのベースURL

def lambda_handler(event, context):
    try:
        # リクエストボディの解析
        body = json.loads(event['body'])
        prompt = body['prompt']
        max_new_tokens = body.get('max_new_tokens', 512)
        do_sample = body.get('do_sample', True)
        temperature = body.get('temperature', 0.7)
        top_p = body.get('top_p', 0.9)

        # FastAPI用のリクエストペイロードを構築
        request_payload = {
            "prompt": prompt,
            "max_new_tokens": max_new_tokens,
            "do_sample": do_sample,
            "temperature": temperature,
            "top_p": top_p
        }

        url = f"{MODEL_ID}/generate"

        # Requestオブジェクトでヘッダーを追加
        req = urllib.request.Request(
            url,
            data=json.dumps(request_payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )

        # FastAPIエンドポイントにPOSTリクエスト送信
        with urllib.request.urlopen(req) as response:
            response_body = json.loads(response.read().decode('utf-8'))

        # レスポンスから値を取得
        generated_text = response_body.get('generated_text')
        response_time = response_body.get('response_time')

        # 成功レスポンスの返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "generated_text": generated_text,
                "response_time": response_time
            })
        }

    except Exception as error:
        print("Error:", str(error))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }

