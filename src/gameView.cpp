#include "../include/gameView.h"

Texture::Texture(int scale) {
    if (scale != 1 && scale != 2 && scale != 4) {
        assert(false && "Invalid scale!");
    }
    scale *= 50;
    textures[Piece::NoneType] = ImageFileFormat::loadFrom(File("./img/piece_0.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::BGeneral] = ImageFileFormat::loadFrom(File("./img/piece_1.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::BAdvisor] = ImageFileFormat::loadFrom(File("./img/piece_2.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::BElephant] = ImageFileFormat::loadFrom(File("./img/piece_3.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::BHorse] = ImageFileFormat::loadFrom(File("./img/piece_4.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::BChariot] = ImageFileFormat::loadFrom(File("./img/piece_5.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::BCannon] = ImageFileFormat::loadFrom(File("./img/piece_6.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::BSoldier] = ImageFileFormat::loadFrom(File("./img/piece_7.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::RGeneral] = ImageFileFormat::loadFrom(File("./img/piece_8.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::RAdvisor] = ImageFileFormat::loadFrom(File("./img/piece_9.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::RElephant] = ImageFileFormat::loadFrom(File("./img/piece_10.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::RHorse] = ImageFileFormat::loadFrom(File("./img/piece_11.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::RChariot] = ImageFileFormat::loadFrom(File("./img/piece_12.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::RCannon] = ImageFileFormat::loadFrom(File("./img/piece_13.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    textures[Piece::RSoldier] = ImageFileFormat::loadFrom(File("./img/piece_14.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
    choiceBox = ImageFileFormat::loadFrom(File("./img/ChoiceBox.png")).rescaled(scale, scale, Graphics::ResamplingQuality::highResamplingQuality);
}

GameView::GameView() {
    background.setSize(1110 * resolution / 2, 1111 * resolution / 2);
    background.setTopLeftPosition(0, 0);
    background.setImage(ImageFileFormat::loadFrom(File("./img/Board.png")).rescaled(1110 * resolution / 2, 1111 * resolution / 2, Graphics::ResamplingQuality::highResamplingQuality));
    addAndMakeVisible(background);

    textures = Texture(resolution);
    auto noColour = juce::Colour((uint8) 0, (uint8) 0, (uint8) 0, 0.0f);
    int x_index[]{111, 222, 333, 444, 555, 666, 777, 888, 999};
    int y_index[]{66, 176, 286, 396, 506, 616, 726, 836, 946, 1056};
    for (auto &x: x_index) {
        x = (int) ((float) x * (resolution / 2.0f));
    }
    for (auto &y: y_index) {
        y = (int) ((float) y * (resolution / 2.0f));
    }
    auto default_image = textures.textures[Piece::NoneType];
    for (size_t i = 0; i < 9; ++i) {
        for (size_t j = 0; j < 10; ++j) {
            pieces[i][j].setSize(resolution * 50, resolution * 50);
            pieces[i][j].setCentrePosition(x_index[i], y_index[j]);
            pieces[i][j].setImages(false, false, true, default_image, 1.0f, noColour, default_image, 0.8f, noColour, default_image, 0.8f, noColour, 0.0f);
            addAndMakeVisible(pieces[i][j]);
        }
    }
    setSize(1110 * resolution / 2, 1111 * resolution / 2);
}

void GameView::draw(std::vector<std::vector<Piece>> grid) {
    auto noColour = juce::Colour((uint8) 0, (uint8) 0, (uint8) 0, 0.0f);
    for (size_t i = 0; i < 9; ++i) {
        for (size_t j = 0; j < 10; ++j) {
            float threshold = grid[i][j] == Piece::NoneType ? 0.0f : 0.6f;
            pieces[i][j].setImages(false, false, true,
                                   textures.textures[grid[i][j].value()], 1.0f, noColour,
                                   textures.textures[grid[i][j].value()], 0.8f, noColour,
                                   textures.textures[grid[i][j].value()], 0.8f, noColour,
                                   threshold);
            addAndMakeVisible(pieces[i][j]);
        }
    }
}

