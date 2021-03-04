package main

import (
    "container/heap"
    "fmt"
    "time"
)

var (
    speed = 100 * time.Millisecond
)

func strToByte(s [][]string) [][]byte {
    ret := make([][]byte, len(s))
    for r := range s {
        ret[r] = make([]byte, len(s[r]))
        for c,v := range s[r] {
            if v == "1" {
                ret[r][c] = byte('1')
            } else if v == "2" {
                ret[r][c] = byte('2')
            } else if v == "3" {
                ret[r][c] = byte('3')
            } else if v == "4" {
                ret[r][c] = byte('4')
            } else if v == "5" {
                ret[r][c] = byte('5')
            } else if v == "6" {
                ret[r][c] = byte('6')
            } else if v == "7" {
                ret[r][c] = byte('7')
            } else if v == "8" {
                ret[r][c] = byte('8')
            } else if v == "9" {
                ret[r][c] = byte('9')
            } else if v == "." {
                ret[r][c] = byte('.')
            } else {
                panic("at the disco")
            }
        }
    }
    return ret
}

func print(board [][]byte) {
    fmt.Printf("\033[0;0H")
    for r := 0; r < 9; r++ {
        if r%3 == 0 {
            fmt.Println("+---+---+---+                             ")
        }
        row := ""
        for c := 0; c < 9; c++ {
            if c%3 == 0 {
                row += "|"
            }
            row += string(rune(board[r][c]))
        }
        row += "|                             "
        fmt.Println(row)
    }
    fmt.Println("+---+---+---+                             ")
    time.Sleep(speed)
}

func main() {
    board := strToByte([][]string{{"8",".",".",".",".",".",".",".","."},{".",".","3","6",".",".",".",".","."},{".","7",".",".","9",".","2",".","."},{".","5",".",".",".","7",".",".","."},{".",".",".",".","4","5","7",".","."},{".",".",".","1",".",".",".","3","."},{".",".","1",".",".",".",".","6","8"},{".",".","8","5",".",".",".","1","."},{".","9",".",".",".",".","4",".","."}})
    print(board)
    solveSudoku(board)
}

func solveSudoku(board [][]byte)  {
    solveSudokuRecurse(board)
}

type Cell struct {
    r, c int        // row and column of the cell
    p map[byte]bool // possibilities for the cell
}

// A SudokuHeap implements heap.Interface and holds Cells.
type SudokuHeap []*Cell

func (h SudokuHeap) Len() int { return len(h) }

func (h SudokuHeap) Less(i, j int) bool {
    return len(h[i].p) < len(h[j].p)
}

func (h SudokuHeap) Swap(i, j int) {
    h[i], h[j] = h[j], h[i]
}

func (h *SudokuHeap) Push(x interface{}) {
    item := x.(*Cell)
    *h = append(*h, item)
}

func (h *SudokuHeap) Pop() interface{} {
    old := *h
    n := len(old)
    item := old[n-1]
    old[n-1] = nil
    *h = old[0 : n-1]
    return item
}

func P(board [][]byte, r, c int) map[byte]bool {
    if board[r][c] != '.' {
        panic("don't call P with filled in location in board")
    }
    p := make(map[byte]bool)
    for n := byte('1'); n <= byte('9'); n++ {
        p[n] = true
    }
    for nc := 0; nc < 9; nc++ {
        if nc == c || board[r][nc] == '.' {
            continue
        }
        delete(p, board[r][nc])
    }
    for nr := 0; nr < 9; nr++ {
        if nr == r || board[nr][c] == '.' {
            continue
        }
        delete(p, board[nr][c])
    }
    for nbr := 0; nbr < 3; nbr++ {
        for nbc := 0; nbc < 3; nbc++ {
            br := (r/3)*3+nbr
            bc := (c/3)*3+nbc
            if (br == r && bc == c) || board[br][bc] == '.' {
                continue
            }
            delete(p, board[br][bc])
        }
    }
    return p
}

func solveSudokuRecurse(board [][]byte) bool {
    // get a heap of objects, representing the cell & possible values.
    // (priority of heap is the negation of the number of possibilities in the cell)
    var h SudokuHeap
    heap.Init(&h)
    for r := 0; r < 9; r++ {
        for c := 0; c < 9; c++ {
            n := board[r][c]
            if n == '.' {
                heap.Push(&h, &Cell{r: r, c: c, p: P(board, r, c)})
            }
        }
    }
    // 1. pop obj off of heap, or return true if no possibilities in heap
    for h.Len() > 0 {
        cell := heap.Pop(&h).(*Cell)
        // 2. When object is popped, update possibilities from board.
        cell.p = P(board, cell.r, cell.c)
        if len(cell.p) == 0 {
            return false
        }
        // 3. if only one possibility, update board and proceed to step 1.
        if len(cell.p) == 1 {
            for n := range cell.p {
                board[cell.r][cell.c] = n
            }
            print(board)
            continue
        }
        // 4. pick a possibility, populate board with value for next hypothetical world
        for p := range cell.p {
            if board[cell.r][cell.c] != '.' {
                panic("cell was popped for a board position that's already filled in.")
            }
            board[cell.r][cell.c] = p
            print(board)
            // 5. call FUNC with copy of board.
            boardDup := make([][]byte, len(board))
            for i := range board {
                boardDup[i] = make([]byte, len(board[i]))
                copy(boardDup[i], board[i])
            }
            // 6. if FUNC returns with true, return true
            if solveSudokuRecurse(boardDup) {
                for i := range boardDup {
                    board[i] = make([]byte, len(boardDup[i]))
                    copy(board[i], boardDup[i])
                 }
                return true
            }
            // 7. if FUNC returns with false, reset board and return to 1.
            board[cell.r][cell.c] = '.'
        }
        return false
    }
    return true
}
