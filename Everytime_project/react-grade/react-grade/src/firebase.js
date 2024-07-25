// src/firebase.js
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getFirestore } from "firebase/firestore";
import { getDatabase } from "firebase/database";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDjr-qoXp_qFKY36r4Vq4GJxUkaiJGwT5g",
  authDomain: "react-grade.firebaseapp.com",
  databaseURL: "https://react-grade-default-rtdb.firebaseio.com",
  projectId: "react-grade",
  storageBucket: "react-grade.appspot.com",
  messagingSenderId: "683711460787",
  appId: "1:683711460787:web:8408d87df34d3aa47907c6",
  measurementId: "G-4ENESM7NMS"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);
const database = getDatabase(app);
const googleProvider = new GoogleAuthProvider();

export { app, analytics, auth, db, database, googleProvider };
