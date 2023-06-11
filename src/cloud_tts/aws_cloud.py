import boto3
import keyring
from contextlib import closing
import os


def load_aws_client():
    return(boto3.Session(
        aws_access_key_id=keyring.get_password("aws_tts","aws_access_key_id"),
        aws_secret_access_key=keyring.get_password("aws_tts","aws_secret_access_key"),
        region_name=keyring.get_password("aws_tts","aws_service_region")).client('polly'))


def get_aws_voices(aws_client, language):
    voices_result = aws_client.describe_voices()
    voices_list = []
    for n, voice in enumerate(voices_result['Voices']):
     voices_list.append(dict({
         "id": n,
         "name": voice['Id'],
         "loc": voice['LanguageCode'],
         "gender": voice['Gender'],
         "rate": "Null",
         "engine": voice['SupportedEngines']}
     ))
    return (voices_list)

def aws_tts(text_blocks, aws_client, aws_voice, aws_engine):
    audio_data_list = []
    for n, text_block in enumerate(text_blocks):
        print(f'Text block {n} of {len(text_blocks)}')
        result = aws_client.synthesize_speech(
            OutputFormat='mp3',
            Text=text_block,
            VoiceId=aws_voice,
            Engine=aws_engine
        )
        if "AudioStream" in result:
            audio_data_list.append(result["AudioStream"])
        else:
            print("Error synthesizing speech")
            return
    return b"".join(audio_data_list)
