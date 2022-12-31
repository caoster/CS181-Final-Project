#ifndef GAMEVIEW_H
#define GAMEVIEW_H

#include "include.h"
#include "gameModel.h"
#include <unordered_map>
#include <JuceHeader.h>

class Texture {
public: // functions
    Texture() = default;

    explicit Texture(int scale);

public: // variables
    std::unordered_map<Piece::Value, juce::Image> textures;
    juce::Image choiceBox;
};

class GameView : public Component {
public:
    GameView();

    void setModel(GameModel *gameModel) { model = gameModel; }

    void draw(Board grid);

    ~GameView() override = default;
private:
    // GUI related
    juce::ImageButton pieces[9][10];
    juce::ImageComponent background;

    GameModel *model{nullptr};
    Texture textures;


    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(GameView)
};

#endif //GAMEVIEW_H
