(* Util - strings *)
let explode s = List.init (String.length s) (String.get s);;

(* Read lines from file *)
let read_lines name: string list =
  let ic = open_in name in
  let try_read () =
    try Some (input_line ic) with End_of_file -> None
  in
  let rec loop acc = match try_read () with
    | Some s -> loop (s :: acc)
    | None -> close_in ic; List.rev acc
  in loop [];;

(* Check if it's a digit *)
let is_digit (a: char): bool =
  match a with
  | x when (List.mem x ['0';'1';'2';'3';'4';'5';'6';'7';'8';'9']) -> true 
  | _ -> false;;

(* Get int[] of all numbers in a line -- supports negative numbers *)
let numbers_in_line (line: string): int list =
  let rec h (line: char list) (acc: int list) (curr: string) (negative: bool): int list =
    match line with
    | c :: rest when c = '-' -> h rest acc curr true
    | c :: rest when is_digit c -> h rest acc (curr ^ (String.make 1 c)) negative
    | c :: rest when curr <> "" -> h rest ((if negative then -int_of_string curr else int_of_string curr) :: acc) "" false
    | c :: rest -> h rest acc "" negative
    | [] when curr <> "" -> (if negative then -int_of_string curr else int_of_string curr) :: acc
    | [] -> acc
  in List.rev (h (explode line) [] "" false);;

(* Get int[][] of numers in lines -- reversed order for performace *)
let numers_in_lines (lines: string list): int list list =
  List.fold_left (fun acc x -> (numbers_in_line x) :: acc) [] lines;; 

(* Print int[] *)
let print_int_xs (xs: int list): unit =
  List.iter (fun x -> print_int x; print_char ' ') xs;
  print_newline ();;

(* Print int[][] *)
let print_int_xss (xss: int list list): unit =
  List.iter (fun x -> print_int_xs x) xss;;

(* Get int[] of change *)
let get_change (xs: int list): int list =
  let rec h (xs: int list) (acc: int list): int list =
    match xs with
    | a :: b :: rest -> h (b :: rest) ((b - a) :: acc)
    | _ -> acc
  in List.rev(h xs []);;

(* Check if all entries are 0 *)
let rec is_all_zeros (xs: int list): bool =
  match xs with
  | a :: rest when a <> 0 -> false
  | a :: rest -> is_all_zeros rest
  | [] -> true;;

(* Get int[][] of changes *)
let get_changes (xs: int list): int list list =
  let rec h (xs: int list) (acc: int list list): int list list =
    match xs with
    | xs when is_all_zeros xs -> (0 :: xs) :: acc
    | xs -> h (get_change xs) (xs :: acc)
  in h xs [];;

(* Extrapolate using change *)
let extrapolate_one (xs: int list) (change: int list): int list =
  let rec h (xs: int list) (change: int list) (acc: int list): int list =
    match xs, change with
    | x :: [], c :: [] -> (x + c) :: x :: acc
    | x :: rest_xs, _ :: rest_change -> h rest_xs rest_change (x :: acc)
    | _, _ -> raise (invalid_arg "Invalid input")
  in List.rev (h xs change []);;

(* Extrapolate a series recursively *)
let extrapolate_series (series: int list): int list list =
  let changes = get_changes series in
  let rec h (changes: int list list) (acc: int list list): int list list =
  match changes with
    | change :: series :: rest -> let extrapolated = (extrapolate_one series change) in h (extrapolated :: rest) (extrapolated :: acc)
    | series :: [] -> acc
    | _ -> raise (invalid_arg "Invalid input")
  in h changes [];;

(* Extrapolate and get the new element *)
let get_extrapolated_last_value (series: int list): int =
  let extrapolated_all = extrapolate_series series in
  List.hd (List.rev (List.hd extrapolated_all));;

(* Get int[] of new values for all series *)
let get_extrapolated_last_values (series: int list list): int list =
  List.fold_left (fun acc x -> (get_extrapolated_last_value x) :: acc) [] series;; 

(* Prepare data *)
let lines: string list = read_lines "input.txt";;
let all_series = numers_in_lines lines;;
let rev_all_series = List.fold_left (fun acc x -> List.rev(x) :: acc) [] all_series;;

(* Ex. 1 *)
print_endline "Ex. 1";;
let new_vals = get_extrapolated_last_values (all_series);;
(* print_int_xs new_vals;; *)

let sum = List.fold_left (fun acc x -> acc + x) 0 new_vals;;
print_int sum;;
print_newline ();;

(* Ex. 2 *)
print_endline "Ex. 2";;
let r_new_vals = get_extrapolated_last_values (rev_all_series);;
(* print_int_xs r_new_vals;; *)

let r_sum = List.fold_left (fun acc x -> acc + x) 0 r_new_vals;;
print_int r_sum;;
print_newline ();;
