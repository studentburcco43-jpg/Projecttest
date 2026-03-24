<?php
// include this at the top of any page that should be protected
session_start();
if (!isset($_SESSION['logged_in']) || $_SESSION['logged_in'] !== true) {
    // not authenticated; send to login page (preserves requested URL could be added later)
    header('Location: login.html');
    exit();
}
