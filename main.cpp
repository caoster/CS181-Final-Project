#include <iostream>
#include "include/utils.h"

int main() {
    auto a = Player(Player::Red);
    std::cout << a.reverse() << std::endl;
    std::cout << a << std::endl;
    return 0;
}