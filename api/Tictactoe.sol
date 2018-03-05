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
        if (last_user != msg.sender) {
            last_user = msg.sender;
            if (msg.sender == firstUser) {
                if (grid[x][y] == 0) {
                grid[x][y] = 1;
                } else {
                return;
                }

            } else {
                if (grid[x][y] == 0) {
                grid[x][y] = 2;
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

    function checkGrid() constant returns (bool){
      for(uint8 b = 0; b < 3; b++){
                for(uint8 a = 0; a < 3; a++){
                    if (grid[b][a]==0) {
                        return true;
                    }
            }
      }
      return false;
    }
    
        function checkGridforWin() constant returns (bool){
            if (((grid[0][0] == grid[0][1]) && (grid[0][1] == grid[0][2] && (grid[0][2]!=0)) || (grid[0][0] == grid[1][0]) && (grid[1][0] == grid[2][0]&& (grid[2][0]!=0)) ||
            (grid[0][0] == grid[1][1]) && (grid[1][1] == grid[2][2])&& (grid[2][2]!=0)) ||
            ( ((grid[2][2] == grid[1][2]) && (grid[1][2] == grid[0][2])&& (grid[2][2]!=0)) || ((grid[2][2] == grid[1][1]) && (grid[1][1] == grid[2][0])&& (grid[2][0]!=0)) ||
            ((grid[2][2] == grid[2][1]) && (grid[2][1] == grid[2][0])&& (grid[2][0]!=0)))){
                return true;
            }
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

}

