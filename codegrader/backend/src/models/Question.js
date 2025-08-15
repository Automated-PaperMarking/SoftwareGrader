const mongoose = require("mongoose");

const TestCaseSchema = new mongoose.Schema({
    input: String,
    expectedOutput: String,
    isHidden: Boolean
});

const QuestionSchema = new mongoose.Schema({
    title: String,
    description: String,
    difficulty: String,
    testCases: [TestCaseSchema]
});

module.exports = mongoose.model("Question", QuestionSchema);
