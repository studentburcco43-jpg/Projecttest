<?php
session_start();
// destroy any existing session data then redirect to login screen
session_destroy();
header('Location: login.html');
exit();
