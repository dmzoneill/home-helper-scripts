<?php

$path = '/series/';
$real_path = realpath($path);
$path_split_count = count(explode("/", $path));
$objects = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($real_path), RecursiveIteratorIterator::SELF_FIRST);

$mmm = [];

function create_season_dir($split, $name) {
	preg_match('/ (([0-9]{1,2})x[0-9]{1,2}) /', $name, $matches);
	if(count($matches) != 3) {
		return null;
	}
	
	$season_dir = array_slice($split, 0, -1);
	$make_dir = implode( "/", $season_dir) . "/Season " . $matches[2];
	//print_r($matches);
	print $make_dir . "\n";
	if(is_dir($make_dir)) return $make_dir;
	if(mkdir($make_dir)) return $make_dir;
	return null;
}

function move_file_season_folder($name) {
	global $path_split_count;
	
	$split = explode("/", $name);
	$split_count = count($split);
	
	if($split_count < $path_split_count + 2) {
		$move_dir = create_season_dir($split, $name);
		if(is_null($move_dir)) {
			print "Dirty: $name\n"; 
			return false;	
		}
		if(rename($name, $move_dir . "/" . $split[$split_count -1])) {
			return $move_dir . "/" . $split[$split_count -1];
		}		
		print "Rename failed: $name\n";
		return false;
	}
	return $name;
}

function check_filename_format($name) {
	global $path_split_count, $mmm;
		
	$split = explode("/", $name);
	$season = explode(" ", $split[$path_split_count])[1];
	$mmm[] = $season;
	//print $season . "\n";
	return
	
	$split_count = count($split);
	
	if($split_count < $path_split_count + 2) {
		$move_dir = create_season_dir($split, $name);
		if(is_null($move_dir)) {
			print "Dirty: $name\n"; 
			return;		
		}
		rename($name, $move_dir . "/" . $split[$split_count -1]);
	}
}


foreach($objects as $name => $object) {
	if(is_dir($name)) continue;
	
	$skip = ['jpg','nfo', 'png', 'hidden', 'srt', 'idx', 'sub', 'smi'];
	$delete = ['DS_Store','txt'];
	$inspect = ['metadata','filename'];
	$info = pathinfo($name);
	
	if(in_array($info['extension'], $delete)) {
		unlink($name);
		print "Delete: $name\n"; 
	 	continue;
	}
		
	if(in_array($info['extension'], $skip)) {
	 	continue;
	}
	
	$correct_name = move_file_season_folder($name);
	if($correct_name == false) {
		continue;
	}
	
	check_filename_format($correct_name);
}


print_r(array_unique($mmm));
