import os
import asyncio
import shutil
from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, UseCurrentSession

async def telethon_to_tdata(session_file, output_dir):
  try:
    client = TelegramClient(session_file)

    tdesk = await client.ToTDesktop(flag=UseCurrentSession)

    session_name = os.path.splitext(os.path.basename(session_file))[0]
    tdata_folder = os.path.join(output_dir, session_name)

    os.makedirs(tdata_folder, exist_ok=True)
    tdesk.SaveTData(tdata_folder)
    
    print(f"Converted {session_file} to {tdata_folder}")

  except Exception as e:
    print(f"Error converting {session_file}: {e}")
    if os.path.exists(tdata_folder):
      shutil.rmtree(tdata_folder)

async def tdata_to_telethon(tdata_folder, output_dir):
  try:
    print(tdata_folder)
    tdesk = TDesktop(tdata_folder)

    session_name = os.path.basename(tdata_folder)
    session_file = os.path.join(output_dir, f"{session_name}.session")

    api = API.TelegramIOS.Generate()
    client = await tdesk.ToTelethon(session_file, UseCurrentSession, api)
    await client.connect()
    await client.PrintSessions()

    print(f"Converted {tdata_folder} to {session_file}")

  except Exception as e:
    print(f"Error converting {tdata_folder}: {e}")
    if os.path.exists(session_file):
      os.remove(session_file)

async def main():
  RED = "\033[31m"
  RESET = "\033[0m"

  print(f'''{RED}   .dMMMb  dMP dMP dMP dMMMMMP dMMMMMMP dMMMMb  dMP dMP dMP 
  dMP" VP dMP dMP amr dMP    dMP   dMP.dMP amr dMK.dMP  
  VMMMb  dMMMMMP dMP dMMMP    dMP   dMMMMK" dMP .dMMMK"   
dP .dMP dMP dMP dMP dMP    dMP   dMP"AMF dMP dMP"AMF  
VMMMP" dMP dMP dMP dMP    dMP   dMP dMP dMP dMP dMP   {RESET}''')
  mode = input("Select mode:\n1) Telethon to tdata\n2) tdata to Telethon\n\n> ")
  if not mode:
    return

  input_dir = input("Enter the directory containing the files: ")
  if not os.path.isdir(input_dir):
    print("Invalid directory!")
    return
  output_dir = input("Enter the output directory: ")

  if mode == "1":
    os.makedirs(output_dir, exist_ok=True)  
    session_files = [f for f in os.listdir(input_dir) if f.endswith(".session")]
    
    if not session_files:
      print("No .session files found in the directory!")
      return

    tasks = [telethon_to_tdata(os.path.join(input_dir, session), output_dir) for session in session_files]
    await asyncio.gather(*tasks)

  elif mode == "2":
    os.makedirs(output_dir, exist_ok=True)
    tdata_folders = [f for f in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, f))]

    if not tdata_folders:
      print("No tdata folders found in the directory!")
      return

    tasks = [tdata_to_telethon(os.path.join(input_dir, folder), output_dir) for folder in tdata_folders]
    await asyncio.gather(*tasks)

  print(f"All conversions completed and saved in {output_dir}")

if __name__ == "__main__":
  asyncio.run(main())
