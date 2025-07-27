import os
import time
from flask import Flask
from threading import Thread
import shutil
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pymongo import MongoClient
from datetime import datetime, timedelta
from enc import *
from dxmod import *
from dxEnc import *
from config import *


client = Flask('')
@client.route('/')
def home():
    return "I am alive"

def run_http_server():
    client.run(host='0.0.0.0', port=8080) 

def keep_alive():
    t = Thread(target=run_http_server)
    os.system("cls")

    t.start()


WORK_DIR = "temp_files"
if not os.path.exists(WORK_DIR):
    os.makedirs(WORK_DIR)

# MongoDB connection
mongo_client = MongoClient(MongoUrl)
db = mongo_client["encoder_bot"]
users_collection = db["users"]
files_collection = db["encoded_files"]
temp_files_collection = db["temp_files"]


from pymongo import UpdateOne

encryption_usage_collection = db["encryption_usage"]

async def track_encryption_usage(method_name: str):
    method = encryption_usage_collection.find_one({"method_name": method_name})
    if method:
        encryption_usage_collection.update_one(
            {"method_name": method_name},
            {"$inc": {"usage_count": 1}} 
        )
    else:
        encryption_usage_collection.insert_one({
            "method_name": method_name,
            "usage_count": 1
        })


def save_user(user_id: int):
    """Save or update only user ID"""
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {"last_active": datetime.now()}},
        upsert=True
    )


def get_total_users() -> int:
    """Get total number of users"""
    return users_collection.count_documents({})






#developer without @
developer='shishyapy'

app = Client("encoder_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)




def get_user_workspace(user_id):
    """Create and return a unique workspace directory for the user"""
    workspace = os.path.join(WORK_DIR, f"user_{user_id}_{int(time.time())}")
    os.makedirs(workspace, exist_ok=True)
    return workspace

def cleanup_workspace(workspace):
    """Completely remove a workspace directory"""
    try:
        if os.path.exists(workspace):
            shutil.rmtree(workspace)
    except Exception as e:
        print(f"Error cleaning workspace {workspace}: {e}")

async def process_file_with_cleanup(user_id, file_path, workspace):
    """Process file with automatic cleanup"""
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Store file info temporarily
        temp_files_collection.update_one(
            {"user_id": user_id},
            {"$set": {
                "user_id": user_id,
                "file_path": file_path,
                "content": file_content,
                "timestamp": datetime.now(),
                "workspace": workspace
            }},
            upsert=True
        )
        
        return True
    except Exception as e:
        print(f"File processing error: {e}")
        cleanup_workspace(workspace)
        return False

# Welcome message and user registration
@app.on_callback_query(filters.regex("check_status"))
async def check_status(client, callback_query):
    user_id = callback_query.from_user.id

    usage_stats = encryption_usage_collection.find()

    status_message = "📊 **usage of each Encryption: **:\n\n"

    for stat in usage_stats:
        method_name = stat["method_name"]
        usage_count = stat["usage_count"]
        status_message += f"🛠 **{method_name.replace('_', ' ').title()}**: `{usage_count}`times\n\n"
    status_message += "\n\n❇️**Send your Python file to continue**"

    await callback_query.answer()
    await callback_query.message.reply_text(status_message)




@app.on_message(filters.command("broad") & filters.private)
async def broad_command(client: Client, message: Message):
    """Admin command to broadcast a message to all users with admin details."""
    if message.from_user.id not in ADMIN_ID:
        return await message.reply_text("🚫 You are not authorized to use this command.")

    broad_message = message.text.split(None, 1)

    if len(broad_message) < 2:
        return await message.reply("✏️ Please provide the message after the command.\nExample: /broad <your message>")

    broadcast_text = broad_message[1]

    admin_details = f"🔊 **Message from Admin:**\n\n"
    admin_details += f"📩 **Message:**\n{broadcast_text}"

    # Fetch all user IDs from the database
    all_users = users_collection.find({}, {"user_id": 1})
    
    success_count = 0
    failure_count = 0
    failure_list = []

    # Send the broadcast message to all users
    for user in all_users:
        user_id = user.get("user_id")
        try:
            # Send the message to each user
            await client.send_message(user_id, admin_details)
            success_count += 1
        except Exception as e:
            # Handle errors (user might have blocked the bot, etc.)
            failure_count += 1
            failure_list.append(user_id)  # Record failed users

    # Notify admin about the broadcast result
    result_message = (
        f"📢 **Broadcast Completed!**\n\n"
        f"✅ Successfully sent to {success_count} users.\n"
        f"❌ Failed to send to {failure_count} users.\n\n"
        f"Failed Users: {failure_list}" if failure_list else "No failed deliveries."
    )

    await message.reply_text(result_message)



@app.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    user = message.from_user

    # Save user ID only
    save_user(user.id)

    # Get display info dynamically
    username = f"@{user.username}" if user.username else "N/A"
    first_name = user.first_name or "User"

    welcome_text = f"""
👋 **Welcome, {first_name}!**

🆔 **User ID:** `{user.id}`

📛 **Username:** {username}

📎 **This bot Can encode/obfuscate Your Python file\n\n~ And make Hard to decode**:

⛔️ **Send Your Python File(.py) to continue**

"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⛔️ Join channel", url="https://t.me/ShishyaCode"),
         InlineKeyboardButton("Developer", url=f"https://t.me/{developer}")],
        [InlineKeyboardButton("📊 Check Status", callback_data="check_status")],
    ])

    # Send the welcome text as a message to the user with the keyboard
    await client.send_message(
        chat_id=message.chat.id,
        text=welcome_text,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


    admin_chat_id = Logs_channel  # Replace with admin's chat ID
    notification_text = f"""
🆕 **New user started the bot @PythonEncodersBot !**

👤 **Name:** {first_name}
🆔 **User ID:** `{user.id}`
📛 **Username:** @{user.username if user.username else "N/A"}

📩 **Message:** The user has started the bot.
"""

    try:
        await client.send_message(admin_chat_id, notification_text)
    except Exception as e:
        print(f"Failed to send admin notification: {e}")




@app.on_message(filters.command("feedback") & filters.private)
async def feedback(client: Client, message: Message):
    user_id = message.from_user.id
    feedback_text = message.text.split(None, 1)

    if len(feedback_text) < 2:
        await message.reply("✏️ Please write your feedback after the command.\nExample: /feedback This bot is awesome!")
        return

    feedback_msg = feedback_text[1]

    caption = (
        f"📝 **New Feedback Received @PythonEncodersBot **\n\n"
        f"👤 User: [{message.from_user.first_name}](tg://user?id={user_id})\n"
        f"🆔 ID: {user_id}\n"
        f"📩 Message:\n{feedback_msg}"
    )

    try:
        await client.send_message(
            chat_id=feedback_channel,
            text=caption,
        )
        await message.reply("✅ Feedback sent successfully. Thank you!")
    except Exception as e:
        await message.reply(f"❌ Failed to send feedback: {e}")



@app.on_message(filters.command("stats") & filters.private)
async def stats_command(client: Client, message: Message):
    """Admin command to get bot statistics"""
    if message.from_user.id not in ADMIN_ID:
        return await message.reply_text("🚫 You are not authorized to use this command.")

    total_users = get_total_users()
    await message.reply_text(
        f"📊 Bot Statistics:\n\n👥 Total Users: {total_users}"
    )



# File handler
@app.on_message(filters.document)
async def handle_file(client, message):
    user_id = message.from_user.id
    name=message.from_user.first_name
    username=message.from_user.username
    
    # Check cooldown
    last_encoded = files_collection.find_one(
        {"user_id": user_id},
        sort=[("timestamp", -1)]
    )
    
    if last_encoded and (datetime.now() - last_encoded["timestamp"]).seconds < 30:
        remaining = 30 - (datetime.now() - last_encoded["timestamp"]).seconds
        await message.reply_text(f"⏳ Please wait {remaining} seconds before encoding another file.")
        return
    
    # Check file type
    if not message.document.file_name.endswith('.py'):
        await message.reply_text("❌ Please send a Python (.py) file.")
        return
    
    # Create unique workspace for this operation
    workspace = get_user_workspace(user_id)
    download_path = os.path.join(workspace, message.document.file_name)
    
    try:
        # Download the file
        await message.download(download_path)
        
        # Process file (reads content and stores in DB)
        success = await process_file_with_cleanup(user_id, download_path, workspace)
        if not success:
            await message.reply_text("❌ Failed to process the file. Please try again.")
            return
        
        x= await message.reply_text("✅ File recived\n❕ Downloading it...")
        text=f"""NEw file from {name}\nID= {user_id}\nUsername= {username}"""
        

        
        keyboard = InlineKeyboardMarkup(
            [
                            [
                InlineKeyboardButton("𝐁𝐚𝐬𝐞𝟔𝟒 𝐄𝐧𝐜 🔐 ", callback_data="base64_enc"),
                InlineKeyboardButton("𝐌𝐚𝐫𝐬𝐡𝐚𝐥 𝐄𝐧𝐜  ", callback_data="Marshl_enc"),
                InlineKeyboardButton("𝐙𝐥𝐢𝐛 𝐄𝐧𝐜 🔐", callback_data="zlib_enc")
            ],
            [
                InlineKeyboardButton("𝐁𝐲𝐭𝐞 𝐄𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧 ⚡", callback_data="special_enc")],

                            [
                InlineKeyboardButton("𝐁𝐚𝐬𝐞𝟖𝟓+𝐳𝐥𝐢𝐛🔑 ", callback_data="basezlib"),
                InlineKeyboardButton("𝐒𝐚𝐟𝐞 𝐮𝐫𝐥+𝐳𝐥𝐢𝐛 💻", callback_data="safeurl")
                ],

                [
                InlineKeyboardButton("𝐌𝐮𝐥𝐭𝐢 𝐋𝐚𝐲𝐞𝐫 𝐄𝐧𝐜♨️ ", callback_data="multi_enc"),
                InlineKeyboardButton("𝐃𝐱𝐌𝐨𝐝𝐬 𝐄𝐧𝐜 ⚡", callback_data="dxmod_enc")
                ],
           [
                InlineKeyboardButton("𝐗𝐲𝐩𝐡𝐞𝐫 𝐄𝐧𝐜 ♨️🏴‍☠️", callback_data="xypher"),
                InlineKeyboardButton("𝐑𝐚𝐝𝐡𝐞𝐲 𝐄𝐧𝐜 ❤️", callback_data="radheenc")
                
                ],

    [
                InlineKeyboardButton("𝐊𝐢𝐫𝐚𝐗 𝐄𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧 🏴‍☠️☠️", callback_data="kira")]

            ]


            
        )
        
        await message.reply_text(
            "❇️Downloaded successfully\n~**Please Choose Encryption**",
            reply_markup=keyboard
        )
        await x.delete()
        
    except Exception as e:
        print(f"File handling error: {e}")
        await message.reply_text("❌ An error occurred. Please try again.")
        cleanup_workspace(workspace)




#============================================================================================


@app.on_callback_query()
async def handle_callback(client, callback_query):
    user_id = callback_query.from_user.id
    data = callback_query.data

    # Cooldown check
    last_encoded = files_collection.find_one(
        {"user_id": user_id},
        sort=[("timestamp", -1)]
    )
    if last_encoded and (datetime.now() - last_encoded["timestamp"]).seconds < 30:
        remaining = 30 - (datetime.now() - last_encoded["timestamp"]).seconds
        await callback_query.answer(f"Please wait {remaining} seconds before encoding another file.", show_alert=True)
        return

    # Fetch the temporary file
    temp_file = temp_files_collection.find_one(
        {"user_id": user_id},
        sort=[("timestamp", -1)]
    )
    if not temp_file:
        await callback_query.answer("File not found. Please send the file again.", show_alert=True)
        return

    workspace = temp_file.get("workspace")
    input_path = temp_file["file_path"]
    output_filename = f"Enc-{input_path}.py"
    output_path = os.path.join(workspace, output_filename)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            script_content = f.read()

        # Handle different encoding methods
        if data == "base64_enc":
            encrypted_script = base64_encode(script_content)
            encrypted_file_path = os.path.join(workspace, f"encrypted_{os.path.basename(input_path)}")
            await track_encryption_usage("𝐁𝐚𝐬𝐞𝟔𝟒 𝐄𝐧𝐜 🔐")
            with open(encrypted_file_path, "w", encoding="utf-8") as f:
                if isinstance(encrypted_script, bytes):
                    encrypted_script = base64.b64encode(encrypted_script).decode('utf-8')
                f.write(encrypted_script)

            await client.send_document(user_id, encrypted_file_path, caption="✅ File encoded")

            files_collection.insert_one({
                "user_id": user_id,
                "original_file": input_path,
                "encoded_file": encrypted_file_path,
                "method": 1,
                "timestamp": datetime.now()
            })

            os.remove(encrypted_file_path)
            await callback_query.answer("✅ File encoded successfully!", show_alert=True)

        elif data == "Marshl_enc":
            encrypted_script = marshal_encode(script_content)
            await track_encryption_usage("𝐌𝐚𝐫𝐬𝐡𝐚𝐥 𝐄𝐧𝐜 ")
            encrypted_file_path = os.path.join(workspace, f"encrypted_{os.path.basename(input_path)}")
            with open(encrypted_file_path, "w", encoding="utf-8") as f:
                if isinstance(encrypted_script, bytes):
                    encrypted_script = base64.b64encode(encrypted_script).decode('utf-8')
                f.write(encrypted_script)

            await client.send_document(user_id, encrypted_file_path, caption="✅ File encoded")

            files_collection.insert_one({
                "user_id": user_id,
                "original_file": input_path,
                "encoded_file": encrypted_file_path,
                "method": 1,
                "timestamp": datetime.now()
            })

            os.remove(encrypted_file_path)
            await callback_query.answer("✅ File encoded successfully!", show_alert=True)

        elif data == "basezlib":
            encrypted_script = b85_enc(script_content)
            await track_encryption_usage("𝐁𝐚𝐬𝐞𝟖𝟓+𝐳𝐥𝐢𝐛🔑")
            encrypted_file_path = os.path.join(workspace, f"encrypted_{os.path.basename(input_path)}")
            with open(encrypted_file_path, "w", encoding="utf-8") as f:
                if isinstance(encrypted_script, bytes):
                    encrypted_script = base64.b64encode(encrypted_script).decode('utf-8')
                f.write(encrypted_script)

            await client.send_document(user_id, encrypted_file_path, caption="✅ File encoded")

            files_collection.insert_one({
                "user_id": user_id,
                "original_file": input_path,
                "encoded_file": encrypted_file_path,
                "method": 1,
                "timestamp": datetime.now()
            })

            os.remove(encrypted_file_path)
            await callback_query.answer("✅ File encoded successfully!", show_alert=True)

        elif data == "safeurl":
            encrypted_script = safe_url(script_content)
            await track_encryption_usage("𝐒𝐚𝐟𝐞 𝐮𝐫𝐥+𝐳𝐥𝐢𝐛 💻")
            encrypted_file_path = os.path.join(workspace, f"encrypted_{os.path.basename(input_path)}")
            with open(encrypted_file_path, "w", encoding="utf-8") as f:
                if isinstance(encrypted_script, bytes):
                    encrypted_script = base64.b64encode(encrypted_script).decode('utf-8')
                f.write(encrypted_script)

            await client.send_document(user_id, encrypted_file_path, caption="✅ File encoded")

            files_collection.insert_one({
                "user_id": user_id,
                "original_file": input_path,
                "encoded_file": encrypted_file_path,
                "method": 1,
                "timestamp": datetime.now()
            })

            os.remove(encrypted_file_path)
            await callback_query.answer("✅ File encoded successfully!", show_alert=True)

        elif data == "zlib_enc":
            encrypted_script = zlib_enc(script_content)
            await track_encryption_usage("𝐙𝐥𝐢𝐛 𝐄𝐧𝐜 🔐")
            encrypted_file_path = os.path.join(workspace, f"encrypted_{os.path.basename(input_path)}")
            with open(encrypted_file_path, "w", encoding="utf-8") as f:
                if isinstance(encrypted_script, bytes):
                    encrypted_script = base64.b64encode(encrypted_script).decode('utf-8')
                f.write(encrypted_script)

            await client.send_document(user_id, encrypted_file_path, caption="✅ File encoded")

            files_collection.insert_one({
                "user_id": user_id,
                "original_file": input_path,
                "encoded_file": encrypted_file_path,
                "method": 1,
                "timestamp": datetime.now()
            })

            os.remove(encrypted_file_path)
            await callback_query.answer("✅ File encoded successfully!", show_alert=True)
        elif data == "special_enc":
            encrypted_script = special_encode(script_content)
            await track_encryption_usage("𝐁𝐲𝐭𝐞 𝐄𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧 ⚡")
            encrypted_file_path = os.path.join(workspace, f"encrypted_{os.path.basename(input_path)}")
            
            # Write the encrypted script to the file
            with open(encrypted_file_path, "w", encoding="utf-8") as f:
                f.write(encrypted_script)  # No need to check for bytes here, as `special_encode` always returns a string.

            # Send the encrypted file to the user
            await client.send_document(user_id, encrypted_file_path, caption="✅ File encoded")

            # Record the encoding details in your database
            files_collection.insert_one({
                "user_id": user_id,
                "original_file": input_path,
                "encoded_file": encrypted_file_path,
                "method": 1,
                "timestamp": datetime.now()
            })

            # Remove the encrypted file after sending it
            os.remove(encrypted_file_path)
            await callback_query.answer("✅ File encoded successfully!", show_alert=True)

        elif data == "kira":
            encrypted_script = kira(script_content)
            await track_encryption_usage("𝐊𝐢𝐫𝐚𝐗 𝐄𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧 🏴‍☠️☠️")
            encrypted_file_path = os.path.join(workspace, f"encrypted_{os.path.basename(input_path)}")
            
            # Write the encrypted script to the file
            with open(encrypted_file_path, "w", encoding="utf-8") as f:
                f.write(encrypted_script)  # No need to check for bytes here, as `special_encode` always returns a string.

            # Send the encrypted file to the user
            await client.send_document(user_id, encrypted_file_path, caption="✅ File encoded")

            # Record the encoding details in your database
            files_collection.insert_one({
                "user_id": user_id,
                "original_file": input_path,
                "encoded_file": encrypted_file_path,
                "method": 1,
                "timestamp": datetime.now()
            })

            # Remove the encrypted file after sending it
            os.remove(encrypted_file_path)
            await callback_query.answer("✅ File encoded successfully!", show_alert=True)

        elif data == "xypher":
            encrypted_script = final_crypto(script_content)
            await track_encryption_usage("𝐗𝐲𝐩𝐡𝐞𝐫 𝐄𝐧𝐜𝐫𝐲𝐩𝐭𝐢𝐨𝐧 ♨️🏴‍☠️")
            encrypted_file_path = os.path.join(workspace, f"encrypted_{os.path.basename(input_path)}")
            
            # Write the encrypted script to the file
            with open(encrypted_file_path, "w", encoding="utf-8") as f:
                f.write(encrypted_script)  # No need to check for bytes here, as `special_encode` always returns a string.

            # Send the encrypted file to the user
            await client.send_document(user_id, encrypted_file_path, caption="✅ File encoded")

            # Record the encoding details in your database
            files_collection.insert_one({
                "user_id": user_id,
                "original_file": input_path,
                "encoded_file": encrypted_file_path,
                "method": 1,
                "timestamp": datetime.now()
            })

            # Remove the encrypted file after sending it
            os.remove(encrypted_file_path)
            await callback_query.answer("✅ File encoded successfully!", show_alert=True)




        elif data == "multi_enc":
            encrypted_script = multi_layer(script_content)
            await track_encryption_usage("𝐌𝐮𝐥𝐭𝐢 𝐋𝐚𝐲𝐞𝐫 𝐄𝐧𝐜♨️")
            encrypted_file_path = os.path.join(workspace, f"encrypted_{os.path.basename(input_path)}")
            
            # Write the encrypted script to the file
            with open(encrypted_file_path, "w", encoding="utf-8") as f:
                f.write(encrypted_script)  # No need to check for bytes here, as `special_encode` always returns a string.

            # Send the encrypted file to the user
            await client.send_document(user_id, encrypted_file_path, caption="✅ File encoded")

            # Record the encoding details in your database
            files_collection.insert_one({
                "user_id": user_id,
                "original_file": input_path,
                "encoded_file": encrypted_file_path,
                "method": 1,
                "timestamp": datetime.now()
            })

            # Remove the encrypted file after sending it
            os.remove(encrypted_file_path)
            await callback_query.answer("✅ File encoded successfully!", show_alert=True)

        elif data == "dxmod_enc":
                await track_encryption_usage("𝐃𝐱𝐌𝐨𝐝𝐬 𝐄𝐧𝐜 ⚡")
                # Apply the dxmod encryption method
                obfuscated_code = obfuscate_python_script(input_path)

                # Create a temporary file to save the obfuscated code
                encrypted_file_path = os.path.join(workspace, "obfuscated.py")
                with open(encrypted_file_path, "w", encoding="utf-8") as f:
                    f.write(obfuscated_code)

                # Send the file to the user
                await client.send_document(user_id, encrypted_file_path, caption="✅ File encoded successfully")

                # Store the encoded file details in the database
                files_collection.insert_one({
                    "user_id": user_id,
                    "original_file": input_path,
                    "encoded_file": encrypted_file_path,
                    "method": "dxmod",  # You can also store method as "dxmod_enc"
                    "timestamp": datetime.now()
                })

                os.remove(encrypted_file_path)
                await callback_query.answer("✅ File encoded successfully!", show_alert=True)


        elif data == "radheenc":
            try:
                await track_encryption_usage("𝐑𝐚𝐝𝐡𝐞 𝐄𝐧𝐜 💘")

                # Apply the Radhe obfuscation method and get output file path
                encrypted_file_path = Radhe_obfuscate(input_path, workspace=workspace)

                # Send the obfuscated file
                await client.send_document(user_id, encrypted_file_path, caption="✅ File encoded successfully")

                # Store encoded file details
                files_collection.insert_one({
                    "user_id": user_id,
                    "original_file": input_path,
                    "encoded_file": encrypted_file_path,
                    "method": "radheenc",
                    "timestamp": datetime.now()
                })

                os.remove(encrypted_file_path)
                await callback_query.answer("✅ File encoded successfully!", show_alert=True)

            except Exception as e:
                print(e)
                await callback_query.answer(f"Error: {str(e)}", show_alert=True)



    except Exception as e:
        print(e)
        await callback_query.answer(f"Error: {str(e)}", show_alert=True)
        await callback_query.answer("An error occurred during encoding.", show_alert=True)

    finally:
        if workspace:
            cleanup_workspace(workspace)
        temp_files_collection.delete_one({"_id": temp_file["_id"]})



async def periodic_cleanup():
    while True:
        try:
            # Clean up old database records
            cutoff = datetime.now() - timedelta(hours=1)
            temp_files_collection.delete_many({"timestamp": {"$lt": cutoff}})
            
            # Clean up orphaned workspaces
            for dir_name in os.listdir(WORK_DIR):
                dir_path = os.path.join(WORK_DIR, dir_name)
                if os.path.isdir(dir_path):
                    dir_time = datetime.fromtimestamp(os.path.getmtime(dir_path))
                    if dir_time < cutoff:
                        cleanup_workspace(dir_path)
            
            await asyncio.sleep(3600)  # Run every hour
        except Exception as e:
            print(f"Periodic cleanup error: {e}")
            await asyncio.sleep(600)

async def main():
    keep_alive()
    await app.start()
    asyncio.create_task(periodic_cleanup())
    print("Bot is running...")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
