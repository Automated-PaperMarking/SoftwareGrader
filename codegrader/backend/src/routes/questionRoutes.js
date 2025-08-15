const express = require("express");
const router = express.Router();
const Question = require("../models/Question");

// Create question
router.post("/", async (req, res) => {
    const question = new Question(req.body);
    await question.save();
    res.json(question);
});

// Get all questions
router.get("/", async (req, res) => {
    const questions = await Question.find();
    res.json(questions);
});

module.exports = router;
