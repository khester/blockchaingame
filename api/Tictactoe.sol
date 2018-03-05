pragma solidity ^0.4.17;

contract Tictactoe {
    int8[3][3] grid;
    bool gridInit;
    address firstUser;
    address secondUser;
    address last_user;
    bool setfirstUser;
    bool setsecondUser;
    address winner;
    bool gameover;
    function getGrid() constant returns (int8[3][3]) {
        return grid;
    }

function initGrid(int8[3][3] grid) public
    {
      if(gridInit) // lockout
          return;
      for(uint8 b = 0; b < 3; b++){
      for(uint8 u = 0; u < 3; u++){

          grid[b][u] = 0;
      }
      }
      gridInit = true;
    }

    function setStep(uint8 x, uint8 y) public {
        if (gameover) {
            return;
        }
        setUsers();

        if (last_user != msg.sender) {
            last_user = msg.sender;
            if (msg.sender == firstUser) {
                if (grid[x][y] == 0) {
                grid[x][y] = 1;
                checkGrid();
                checkGridforWin();
                } else {
                return;
                }

            } else {
                if (grid[x][y] == 0) {
                grid[x][y] = 2;
                checkGrid();
                checkGridforWin();
                } else {
                return;
                }

            }
        } else {
        return;
        }
    }

    function gridstate() constant returns (int8[3][3]) {
        return grid;
    }

    function getOver() constant returns (bool) {
        return gameover;
    }

    function getWinner() constant returns (address) {
        return winner;
    }


    function checkGrid() {
      for(uint8 b = 0; b < 3; b++){
                for(uint8 a = 0; a < 3; a++){
                    if (grid[b][a]==0) {
                        return;
                    }
            }
      }
      gameover = true;
      return;
    }

        function checkGridforWin() {
            if (((grid[0][0] == grid[0][1]) && (grid[0][1] == grid[0][2] && (grid[0][2]!=0)) || (grid[0][0] == grid[1][0]) && (grid[1][0] == grid[2][0]&& (grid[2][0]!=0)) ||
            (grid[0][0] == grid[1][1]) && (grid[1][1] == grid[2][2])&& (grid[2][2]!=0)) ||
            ( ((grid[2][2] == grid[1][2]) && (grid[1][2] == grid[0][2])&& (grid[2][2]!=0)) || ((grid[2][2] == grid[1][1]) && (grid[1][1] == grid[2][0])&& (grid[2][0]!=0)) ||
            ((grid[2][2] == grid[2][1]) && (grid[2][1] == grid[2][0])&& (grid[2][0]!=0))) || ((grid[1][0] == grid[1][1]) && (grid[1][1] == grid[1][2])&& (grid[1][0]!=0))) {
                winner = msg.sender;
                gameover = true;
                return;
            }
            return;
        }

    function setUsers() public {
        if (setfirstUser==true) {
            secondUser = msg.sender;
            setsecondUser = true;
        } else {
            firstUser = msg.sender;
            setfirstUser = true;
        }
    }
 q


