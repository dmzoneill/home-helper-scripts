<?php

function Scan($dir) {
    $tree = glob(rtrim($dir, '/') . '/*');
    if (is_array($tree)) {
        foreach($tree as $file) {
	    echo $file . "\n";
	    $parts = explode("/", $file);
	    $q = $parts[count($parts) - 1];
	    $filebot = "filebot -r -rename --db TheTVDB --action move --conflict auto --q \"$q\" \"$file\"";
	    echo $filebot . "\n";
	    echo shell_exec($filebot);
        }
    }
}

Scan("/series");
