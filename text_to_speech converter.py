import tkinter as tk
import boto3
import os
import sys
from tempfile import gettempdir
from contextlib import closing


root=tk.Tk()
root.geometry("400x400")
root.title("T2S-Con Amazon Polly")
textExample=tk.Text(root,height=10)
textExample.pack()

def getText():
    aws_mag_con=boto3.session.Session(profile_name='demo_user')
    client=aws_mag_con.client(service_name='polly',region_name='us-east-1')
    result=textExample.get("1.0","end")
    print(result)
    response=client.synthesize_speech(Text=result,Engine='neural',OutputFormat='mp3',VoiceId='Joanna')
    print(response)
    if "AudioStream" in response:
        with closing(response['AudioStream']) as stream:
            output = os.path.join(gettempdir(), "speech.mp3")
            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)

    else:
        print("Could not stream audio")
        sys.exit(-1)
    if sys.platform=='win32':
        os.startfile(output)
btnRead=tk.Button(root, height=1, width=10, text="ReadIt",command=getText)

btnRead.pack()


root.mainloop()