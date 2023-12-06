(* Util - strings *)
let explode s = List.init (String.length s) (String.get s);;
let implode cl = String.init (List.length cl) (List.nth cl);;

(* Read lines from file *)
let read_lines name: string list =
  let ic = open_in name in
  let try_read () =
    try Some (input_line ic) with End_of_file -> None
  in
  let rec loop acc = match try_read () with
    | Some s -> loop (s :: acc)
    | None -> close_in ic; List.rev acc
  in
  loop [];;

(* Check if it's a digit *)
let is_digit (a: char): bool =
  match a with
  | x when (List.mem x ['0';'1';'2';'3';'4';'5';'6';'7';'8';'9']) -> true 
  | _ -> false;;

(* Get a int[] of all numbers in a line -- note: reverse order for performance *)
let numbers_in_line (line: string): int list =
  let rec h (line: char list) (acc: int list) (curr: string): int list =
    match line with
    | c :: rest when is_digit c -> h rest acc (curr ^ (String.make 1 c))
    | c :: rest when curr <> "" -> h rest ((int_of_string curr) :: acc) ""
    | c :: rest -> h rest acc ""
    | [] when curr <> "" -> (int_of_string curr) :: acc
    | [] -> acc
  in
  h (explode line) [] "";;

(* Get a int comprised of all digits in a line, ignoring the rest *)
let line_to_int (line: string): int =
  let rec h (line: char list) (curr: string): int =
    match line with
    | c :: rest when is_digit c -> h rest (curr ^ (String.make 1 c))
    | c :: rest -> h rest curr
    | [] -> int_of_string curr
  in h (explode line) "";;

(* Print int[] *)
let print_int_list (xs: int list): unit =
  List.iter (fun x -> print_int x; print_char ' ') xs;
  print_newline ();;

(* int[] of all possible distances in a race *)
let possible_distances (time: int): int list =
  let rec h (hold_time: int) (acc: int list): int list =
    match hold_time with
    | n when n <= time -> h (n + 1) (((time - n) * n) :: acc)
    | n -> acc
  in h 0 [];;

(* Count ways to beat a race *)
let count_ways_to_win (time: int) (record_distance: int): int =
  let rec h (distances: int list) (acc: int): int =
    match distances with
    | d :: rest when d > record_distance -> h rest (acc + 1)
    | d :: rest -> h rest acc
    | [] -> acc
  in h (possible_distances time) 0;;

(* int[] of number of ways to win in races *)
let count_ways_to_win_all (time_array: int list) (distance_array: int list): int list =
  let rec h (time_array: int list) (distance_array: int list) (acc: int list): int list =
    match time_array, distance_array with
    | t :: rest_ta, d :: rest_da -> h rest_ta rest_da ((count_ways_to_win t d) :: acc)
    | [], [] -> acc
    | _, _ -> raise (invalid_arg "Invalid input: time and distance array have different length")
  in h time_array distance_array [];;

(* Prepare data *)
let lines: string list = read_lines "input.txt";;
let time_array = numbers_in_line (List.nth lines 0);;
(* print_int_list time_array;; *)

let distance_array = numbers_in_line (List.nth lines 1);;
(* print_int_list distance_array;; *)

(* Ex. 1 *)
print_endline "Ex. 1: ";;
let ways_to_win_list = count_ways_to_win_all time_array distance_array;;
(* print_int_list ways_to_win_list;; *)

let multiplied = List.fold_left (fun acc x -> acc*x) 1 ways_to_win_list;;
print_int multiplied;;
print_newline ();;

(* Ex. 2 *)
print_endline "Ex. 2: ";;
let time = line_to_int (List.nth lines 0);;
let distance = line_to_int (List.nth lines 1);;

print_int (count_ways_to_win time distance);;
print_newline ();;
