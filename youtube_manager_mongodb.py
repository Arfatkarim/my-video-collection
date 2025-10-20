from tkinter import *
from tkinter import messagebox
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb+srv://md_arfat_karim:arfat_karim@cluster0.psi2qmz.mongodb.net/ytmanager")
db = client["ytmanager"]
video_collection = db["videos"]

def add_video():
    name = name_entry.get()
    time = time_entry.get()
    if not name or not time:
        messagebox.showwarning("Warning", "Please fill all fields!")
        return
    video_collection.insert_one({"name": name, "time": time})
    messagebox.showinfo("Success", f"Video '{name}' added successfully!")
    name_entry.delete(0, END)
    time_entry.delete(0, END)
    list_videos()

def list_videos():
    videos_list.delete(0, END)
    for video in video_collection.find():
        videos_list.insert(END, f"{video['_id']} | {video['name']} | {video['time']}")

def update_video():
    selected = videos_list.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a video to update!")
        return
    video_data = videos_list.get(selected[0])
    video_id = video_data.split('|')[0].strip()
    new_name = name_entry.get()
    new_time = time_entry.get()
    if not new_name or not new_time:
        messagebox.showwarning("Warning", "Please fill all fields!")
        return
    result = video_collection.update_one({"_id": ObjectId(video_id)}, {"$set": {"name": new_name, "time": new_time}})
    if result.matched_count:
        messagebox.showinfo("Success", "Video updated successfully!")
        name_entry.delete(0, END)
        time_entry.delete(0, END)
        list_videos()
    else:
        messagebox.showerror("Error", "Video not found!")

def delete_video():
    selected = videos_list.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Select a video to delete!")
        return
    video_data = videos_list.get(selected[0])
    video_id = video_data.split('|')[0].strip()
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this video?")
    if confirm:
        result = video_collection.delete_one({"_id": ObjectId(video_id)})
        if result.deleted_count:
            messagebox.showinfo("Success", "Video deleted successfully!")
            list_videos()
        else:
            messagebox.showerror("Error", "Video not found!")

root = Tk()
root.title("Youtube Manager App")

Label(root, text="Video Name:").grid(row=0, column=0, padx=10, pady=5)
name_entry = Entry(root, width=30)
name_entry.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Video Time:").grid(row=1, column=0, padx=10, pady=5)
time_entry = Entry(root, width=30)
time_entry.grid(row=1, column=1, padx=10, pady=5)

Button(root, text="Add Video", command=add_video, width=15, bg="lightgreen").grid(row=2, column=0, padx=10, pady=5)
Button(root, text="Update Video", command=update_video, width=15, bg="lightblue").grid(row=2, column=1, padx=10, pady=5)
Button(root, text="Delete Video", command=delete_video, width=15, bg="red").grid(row=3, column=0, padx=10, pady=5)
Button(root, text="Refresh List", command=list_videos, width=15).grid(row=3, column=1, padx=10, pady=5)

videos_list = Listbox(root, width=60)
videos_list.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

list_videos()
root.mainloop()
