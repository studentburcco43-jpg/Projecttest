<?php
session_start();

// simple hard‑coded demo credentials – change for real app
$validEmail = 'demo@grimeguys.com';
$validPass  = 'demo123';

// accept either email or username param for backwards compatibility
$email   = $_POST['email']   ?? $_POST['username'] ?? '';
$password= $_POST['password'] ?? '';

if ($email === $validEmail && $password === $validPass) {
    $_SESSION['logged_in'] = true;
    // once logged in send user to home page
    header('Location: index.html');
    exit();
} else {
    // redirect back to login with error flag
    header('Location: login.html?error=1');
    exit();
}
?>
