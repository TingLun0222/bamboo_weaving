<?php
    require_once 'login.php';
    $game_id = $_POST['game_id'];
    try
    {
        $pdo = new PDO($attr, $user, $pass);
    }
    catch(PDOException $e)
    {
        die(json_encode(array('result' => False)));
        throw new PDOException($e->getMessage(), (int)$e->getCode());
    }
    $query = "SELECT * FROM return_json";
    $fetch = $pdo->query($query);
    $flag = False;
    while($row = $fetch->fetch())
    {
        if($row['game_id']==$game_id)
        {
            // $arr  = array ( 'game_id' => $json->{'game_id'} , 'topic_id' => $json->{'topic_id'} , 'level_id' => intval($level_id) , 'photo' => $content , 
            //                 'percent' => $json->{'percent'} , 'number' => $json->{'number'} , 'wrong_area' => $json->{'wrong_area'}); 
            $flag = True;
            echo json_encode(array('result' => $flag,'data' => json_decode($row['json'])));
            // echo $row['json'];
        } 
    }
    if(!$flag)
    {
        die(json_encode(array('result' => False)));
    }
    $query = "DELETE FROM return_json WHERE game_id=$game_id";
    $delete = $pdo->query($query);
?>