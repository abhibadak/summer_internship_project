require('dotenv').config();
const express = require('express');
const multer = require('multer');
const nodemailer = require('nodemailer');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.static('public')); // Serve frontend

const upload = multer(); // Store files in memory

// Email setup (using Gmail)
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL,
    pass: process.env.PASSWORD
  }
});

// API endpoint
app.post('/send', upload.single('photo'), (req, res) => {
  const { email, message } = req.body;
  const photo = req.file;

  transporter.sendMail({
    from: process.env.EMAIL,
    to: email,
    subject: 'Photo from Camera',
    text: message,
    attachments: [{
      filename: 'photo.jpg',
      content: photo.buffer
    }]
  }, (err) => {
    if (err) return res.status(500).send('Failed to send');
    res.send('Email sent!');
  });
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));