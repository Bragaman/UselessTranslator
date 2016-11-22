# UselessTranslator 
Useless translator for useless language. This is course project. Language use for system of manage robot in cell maze. Maze is a square. Robot can move to neighbor, cell if it is empty.
 

## Lanuage description  
  * `N` - is variable number without repetition.
  * `I` - index of array (int)
  * `ID` -> `.N | ,N | $N ` ?! maybe arrays
  * one line - one statement
  
  
1. Literals
  * Integer `[0-9]{1,}`
  * Boolean `T|F`

2. Variables   
  * Integer `,N`
  * Bool  `.N`
  * Procedures `$N`
  * Labels `~N`
  * Interer array
    * `,N:`       ->    `int aN[0];`
    * `,N:I1`     ->    `int aN[I1];`
    * `,N:I1-I2`  ->    `int aN[I1][I2];  `   
  * Bool array
    * `.N:`       ->    `bool aN[0];`
    * `.N:I1`     ->    `bool aN[I1];`
    * `.N:I1-I2`  ->    `bool aN[I1][I2]; `    
  * Procedures array
    * `$N:`       ->    `func aN[0];`
    * `$N:I1`     ->    `func aN[I1];`
    * `$N:I1-I2`  ->    `func aN[I1][I2];`
    
3. Operators
  * Arithmetical (int)
    * increment `,#N` -> `aN += 1`
    * decrement `,*N` -> `aN -= 1`
  * Logic (bool)
    * logical nor: `.#(logic exp)` !?
  * Assigment `<-`
  * Comparison `<exp> eq <const>`. Three types: logic, int, proc
  * Cycles `(<logic exp>)<cycle operator>{statements}' ?!   
    Note: I dont know what should I use how a cycle operator 
  * Conditions `[<logic exp>] please ~N`  ?! need to know, can I do so?   
    if logic exp is true go to label
  * pass operator `np`. This is python `pass`
  * binding operator `ID @ $N`. bind ID to procedure with the following features:
    * binding many id to many procedure
    * recursive binding is forbidden (return `F`)
    * on handling binded ID: at first call proc, after that return ID value
  * unbinding operator `ID % $N` (return `T`)

4. Operators for manage robot 
  * move robot to one cell on selected direction `mf | mb | mr | ml`, return `T` if robot can do it, else `F`
  * teleport robot to another random cell `tp`, robot has limited quantity try use `tp`, after use this command robot dont know his position.
    
  
