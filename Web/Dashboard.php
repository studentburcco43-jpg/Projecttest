<?php
// simple redirect or logout alias
session_start();
if (isset($_SESSION['logged_in']) && $_SESSION['logged_in'] === true) {
    // if someone visits dashboard, just forward them to home
    header('Location: index.html');
} else {
    header('Location: login.html');
}
exit();
?>