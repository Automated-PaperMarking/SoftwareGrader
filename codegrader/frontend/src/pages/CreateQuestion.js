import React, { useState } from "react";
import axios from "axios";

export default function CreateQuestion() {
    const [formData, setFormData] = useState({
        title: "",
        description: "",
        difficulty: "",
        testCases: []
    });

    const handleSubmit = async () => {
        await axios.post("http://localhost:5000/api/questions", formData);
        alert("Question created!");
    };

    return (
        <div>
            <h2>Create Question</h2>
            <input placeholder="Title" onChange={e => setFormData({...formData, title: e.target.value})} />
            <textarea placeholder="Description" onChange={e => setFormData({...formData, description: e.target.value})}></textarea>
            <button onClick={handleSubmit}>Save</button>
        </div>
    );
}
