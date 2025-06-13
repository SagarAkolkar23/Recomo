# 🎬📚 Recomo – Movie & Book Recommendation App

Recomo is a smart recommendation platform that suggests **personalized movies and books** based on your **mood** and **preferences** using **Gemini API**. Built with a clean and responsive interface, Recomo ensures a smooth user experience across devices.

<br>

![Recomo Banner](https://i.imgur.com/NmUjM6R.png) <!-- Replace with your actual banner or app screenshot -->

---

## 🚀 Features

✅ AI-powered recommendation system  
✅ Movie or book suggestions based on mood  
✅ Clean, mobile-friendly UI using Tailwind CSS  
✅ Displays poster, title, and description for each result  
✅ Stores user inputs and history (MongoDB)  
✅ Fast and interactive frontend using JavaScript  

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML5, CSS3, Tailwind CSS, JavaScript |
| **Backend** | Flask (Python), RESTful API |
| **Database** | MongoDB Atlas |
| **AI Integration** | Gemini API (Google Generative AI) |

---


## 🧠 How It Works

1. User selects:
   - Mood (e.g., Happy, Sad, Curious)
   - Genre (optional)
   - Type (Book or Movie)

2. The input is sent to **Gemini API**, which returns 5 personalized recommendations.

3. Results include:
   - Title
   - Poster
   - Short Description

4. Results are saved to user history in **MongoDB** for future access (if logged in).


