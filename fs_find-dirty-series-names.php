<?php

function startsWith( $haystack, $needle ) {
    $length = strlen( $needle );
    return substr( strtolower($haystack), 0, $length ) === strtolower($needle);
}

function endsWith( $haystack, $needle ) {
    $length = strlen( $needle );
    if( !$length ) {
        return true;
    }
    return substr( $haystack, -$length ) === $needle;
}

// recursive directory scan
function recursiveScan($dir) {
    $tree = glob(rtrim($dir, '/') . '/*');
    if (is_array($tree)) {
        foreach($tree as $file) {
            if (is_dir($file)) {
                //echo $file . "\n";
                recursiveScan($file);
            } elseif (is_file($file)) {
                if(endsWith($file, "poster.jpg")) continue;
                if(endsWith($file, "folder.jpg")) continue;
                if(endsWith($file, "banner.jpg")) continue;
                if(endsWith($file, "fanart.jpg")) continue;
                if(endsWith($file, "logo.jpg")) continue;
                if(endsWith($file, "landscape.jpg")) continue;
                if(endsWith($file, "clearart.png")) continue;
                if(endsWith($file, "logo.png")) continue;
                if(endsWith($file, "tvshow.nfo")) continue;

                $parts = explode("/", $file);

                $correct_series_name = startsWith($parts[count($parts) -1], $parts[count($parts) -3]);
                $correct_series_name_nospaces = startsWith($parts[count($parts) -1], str_replace(" ", "", $parts[count($parts) -3]));

                if( $correct_series_name == false && $correct_series_name_nospaces == false) {
                    echo $file . "\n";
                }
                else {
                    //echo ".";
                }
            }
        }
    }
}


function Scan($dir) {
    $tree = glob(rtrim($dir, '/') . '/*');
    if (is_array($tree)) {
        foreach($tree as $file) {
            //echo $file . "\n";
            recursiveScan($file);
        }
    }
}

Scan("/series");
