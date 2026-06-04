<?php
    require_once 'login.php';
    require_once 'download.php';
    if
    ( isset($_POST['email']) &&
        isset($_POST['game_id']) &&
        isset($_POST['topic_id']) &&
        isset($_POST['level_id']) &&
        isset($_POST['url']) 
    )
    {
        $email = $_POST['email'];
        $game_id = $_POST['game_id'];
        $topic_id = $_POST['topic_id'];
        $level_id = $_POST['level_id'];
        $filepath = 'C:/xampp/htdocs/';
        $url = $_POST['url'];
        $imgname = 'url.jpg';
        $analyze_img='test_analyze.exe';
        $Ans=$topic_id."-".$level_id.'.PNG';
        $exam='exam/'.$Ans;
        if(! file_exists($exam))
        {
            die(json_encode(array('result' => False)));
        }
        if(getImg($url))
        {
            if(file_exists($analyze_img))
                passthru($analyze_img.$exam);
            else
            {
                // echo "not_file_exists";
                die(json_encode(array('result' => False)));
            }
            try
            {
                $json = json_decode(file_get_contents ('./return_data.json'));
            }
            catch(Exception $e)
            {
                // echo "not_return_data";
                die(json_encode(array('result' => False)));
            }
            $content = base64_encode(file_get_contents($imgname));
            if(is_file($imgname))
                unlink($imgname);
            $arr  = array ( 'game_id' => $game_id , 'topic_id' => intval($topic_id) , 'level_id' => intval($level_id) , 'photo' => $content , 
                            'percent' => $json->{'percent'} , 'number' => $json->{'number'} , 'wrong_area' => $json->{'wrong_area'}); 
            #創建SQL物件
            try
            {
                $pdo = new PDO($attr, $user, $pass);
            }
            catch(PDOException $e)
            {
                throw new PDOException($e->getMessage(), (int)$e->getCode());
                die(json_encode(array('result' => False)));
            }
            $ret = json_encode($arr);
            $query = "INSERT INTO return_json(game_id,json) VALUES($game_id ,'$ret')";
            $con = $pdo->query($query);
            echo json_encode(array('result' => True));
            //if(file_exists('./return_data.json'))
                //unlink('./return_data.json');
        }else
        {
            echo json_encode(array('result' => False));
        }
    }
    // else
    // {
    //     echo ('Data input error');
    // }
?>