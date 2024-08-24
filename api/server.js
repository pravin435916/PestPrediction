const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 8000;
// const DB = _URL || 'your-default-mongodb-url-here';

// Middleware
app.use(bodyParser.json());
app.use(cors());

// Connect to MongoDB
mongoose.connect(process.env.DB, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log("MongoDB Connected"))
.catch(err => console.error("MongoDB connection error:", err));

// Define schemas and models
const postSchema = new mongoose.Schema({
  name: { type: String, required: true, default: "anonymous" },
  msg: { type: String, required: true },
  rating: { type: Number, required: true }
});

const userSchema = new mongoose.Schema({
  email: { type: String, required: true }
});

const Post = mongoose.model('Post', postSchema);
const User = mongoose.model('User', userSchema);

// Routes
app.get('/api/posts', async (req, res) => {
  try {
    const posts = await Post.find();
    res.json({ success: true, data: posts });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Error fetching posts', error: err.message });
  }
});

app.post('/api/posts', async (req, res) => {
  try {
    const { msg, rating } = req.body;
    const post = new Post({ msg, rating });
    await post.save();
    res.json({ success: true, data: post });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Error creating post', error: err.message });
  }
});

app.post('/api/email', async (req, res) => {
  try {
    const { email } = req.body;
    const user = new User({ email });
    await user.save();
    res.json({ success: true, data: user });
  } catch (err) {
    res.status(500).json({ success: false, message: 'Error saving email', error: err.message });
  }
});

app.post('/chatbot', (req, res) => {
  const { message } = req.body;
  const lowercaseMessage = message.toLowerCase();

  const responsePatterns = [
    { pattern: 'hello', reply: 'Hi there!' },
    { pattern: 'hi', reply: 'Hello!' },
    { pattern: 'how are you', reply: "I'm just a bot, but I'm doing well!" },
    { pattern: 'fuck', reply: "I'm sorry, I cannot respond to offensive language." },
    { pattern: 'what is your name', reply: "I'm a chatbot, you can call me HopeAI" },
    { pattern: 'who created you', reply: "I was created by Pravin" },
    { pattern: 'who designed you', reply: "I was Designed by Vansh" },
    { pattern: 'what can you do', reply: "I can answer questions, provide information, and engage in conversation." },
    { pattern: 'where are you from', reply: "I exist in the digital realm, so I don't have a physical location." },
    { pattern: 'tell me a joke', reply: "Why don't scientists trust atoms? Because they make up everything!" },
  ];

  const matchedPattern = responsePatterns.find(({ pattern }) => lowercaseMessage.includes(pattern));
  const response = matchedPattern ? matchedPattern.reply : "I'm sorry, I don't understand.";

  setTimeout(() => {
    res.json({ success: true, response });
  }, 1500);
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
