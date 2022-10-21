<?php
    function getImg($url = "", $filename = 'C:/xampp/htdocs/url.jpg')
    {
    //去除URL連線上面可能的引號
    //$url = preg_replace( '/(?:^['"] |['"/] $)/', '', $url );
    $hander = curl_init();
    $fp = fopen($filename,'wb');
    $options = array(
        CURLOPT_URL => $url, 
        CURLOPT_FILE => $fp,
        CURLOPT_HEADER => false,
        CURLOPT_FOLLOWLOCATION => true,
        CURLOPT_TIMEOUT => 60,
    ); 
    curl_setopt_array($hander, $options); 
    curl_exec($hander);
    ob_clean();
    flush();
    curl_close($hander);
    fclose($fp);
    return true;
    }
    // function download($url, $filepath = 'C:/xampp/htdocs/')
    // {
    // $ch = curl_init();
    // $options = array(
    //         CURLOPT_URL => $url, 
    //         CURLOPT_RETURNTRANSFER => 1,
    //         CURLOPT_CONNECTTIMEOUT => 30,
    //         // CURLOPT_FILE => $fp,
    //         // CURLOPT_HEADER => false,
    //         // CURLOPT_FOLLOWLOCATION => true,
    //         // CURLOPT_TIMEOUT => 60,
    //     ); 
    // curl_setopt_array($ch, $options);
    // $file = curl_exec($ch);
    // ob_clean();
    // flush();
    // curl_close($ch);
    // $filename = pathinfo($url, PATHINFO_BASENAME);
    // $resource = fopen($filepath . $filename, 'wb');
    // fwrite($resource, $file);
    // fclose($resource);
    // }
?>