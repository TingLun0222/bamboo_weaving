<?php
require_once 'login.php';
require_once 'download.php';

// Error handling function
function die_with_error() {
    echo json_encode(array('result' => False));
    die();
}

// Check if all POST variables are set
$required_params = ['email', 'game_id', 'topic_id', 'level_id', 'url'];
foreach ($required_params as $param) {
    if (!isset($_POST[$param])) {
        die_with_error();
    }
}

$email = $_POST['email'];
$game_id = $_POST['game_id'];
$topic_id = $_POST['topic_id'];
$level_id = $_POST['level_id'];
$url = $_POST['url'];

$filepath = 'C://xampp//htdocs//';
$imgname = 'url.jpg';
$examFolder = $topic_id."//".$level_id.'//';
$exam = $filepath.'exam//'.$AnsFolder;
$Ans = $exam.$examFolder.'answer.png';
$Dims = $exam.$examFolder.'dimensions.json';


if(! file_exists($exam)) {
    die_with_error();
}

if(getImg($url)) {
    $path='lenandwei_analyze.py ';
    if(! file_exists($path)) {
        die_with_error();
    }

    // Execute the Python script
    passthru($path.$Ans.' '.$Dims);

    // Load the JSON result from the Python script
    try {
        $json = json_decode(file_get_contents ('./return_data.json'));
    } catch(Exception $e) {
        die_with_error();
    }

    $content = base64_encode(file_get_contents($imgname));

    $arr = array (
        'game_id' => $game_id,
        'topic_id' => intval($topic_id),
        'level_id' => intval($level_id),
        'photo' => $content,
        'percent' => $json->{'percent'},
        'number' => $json->{'number'},
        'wrong_area' => $json->{'wrong_area'}
    );

    // Connect to the database and save the JSON data
    try {
        $pdo = new PDO($attr, $user, $pass);
        $ret = json_encode($arr);
        $query = "INSERT INTO return_json(game_id,json) VALUES(:game_id, :json_data)";
        $stmt = $pdo->prepare($query);
        $stmt->execute(['game_id' => $game_id, 'json_data' => $ret]);
        echo json_encode(array('result' => True));
    } catch(PDOException $e) {
        die_with_error();
    }
} else {
    die_with_error();
}

?>