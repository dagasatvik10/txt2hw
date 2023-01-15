from utils.tests import faker


def mock_s3_generate_presigned_post():
    print("mock presigned url")
    return {
        "fields": {
            "Content-Type": "image/png",
            "acl": "private",
            "key": f"files/{faker.unique.md5(raw_output=False)}.png",
            "policy": "some-long-base64-string",
            "x-amz-algorithm": "AWS4-HMAC-SHA256",
            "x-amz-credential": "AKIASOZLZI5FJDJ6XTSZ/20220405/eu-central-1/s3/aws4_request",
            "x-amz-date": f"{faker.date(pattern='%Y%m%dT%H%M%SZ')}",
            "x-amz-signature": "7d8be89aabec12b781d44b5b3f099d07be319b9a41d9a9c804bd1075e1ef5735",
        },
        "url": "https://txt2hw.satvikdaga.com/",
    }
