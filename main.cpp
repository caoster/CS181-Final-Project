#include "MinimaxAgent/MinimaxAgent.h"
#include "RandomAgent/RandomAgent.h"
#include "HumanAgent/HumanAgent.h"
#include "MCTS/MCTSAgent.h"
#include "include/gameView.h"
#include "include/include.h"
#include <JuceHeader.h>
#include <thread>

class Application : public juce::JUCEApplication {
public:
    Application() = default;

    const juce::String getApplicationName() override { return "Chinese Chess"; }

    const juce::String getApplicationVersion() override { return "1.0.0"; }

    void initialise(const juce::String &) override {
        view = new GameView();
        mainWindow = new MainWindow(getApplicationName(), view, *this);
        if (config.red == "RandomAgent") {
            red = new RandomAgent({Player::Red});
        } else if (config.red == "MinimaxAgent") {
            red = new MinimaxAgent({Player::Red}, 2);
        } else if (config.red == "HumanAgent") {
            red = new HumanAgent({Player::Red});
        } else if (config.red == "MCTSAgent") {
            red = new MCTSAgent({Player::Red});
        } else {
            exit(123);
        }
        if (config.black == "RandomAgent") {
            black = new RandomAgent({Player::Black});
        } else if (config.black == "MinimaxAgent") {
            black = new MinimaxAgent({Player::Black}, 2);
        } else if (config.black == "HumanAgent") {
            black = new HumanAgent({Player::Black});
        } else if (config.black == "MCTSAgent") {
            black = new MCTSAgent({Player::Black});
        } else {
            exit(123);
        }
        model = new GameModel(view, red, black);
        red->setGameModel(model);
        black->setGameModel(model);
        model->startThread(juce::Thread::Priority::highest);
    }

    void shutdown() override {
        delete mainWindow;
        delete view;
        delete model;
        delete red;
        delete black;
    }

private:
    class MainWindow : public juce::DocumentWindow {
    public:
        MainWindow(const juce::String &name, juce::Component *c, JUCEApplication &a) : DocumentWindow(name,
                                                                                                      juce::Colours::darkgrey,
                                                                                                      juce::DocumentWindow::allButtons),
                                                                                       app(a) {
            setUsingNativeTitleBar(true);
            setContentOwned(c, true);
            setResizable(false, false);
            centreWithSize(getWidth(), getHeight());
            setVisible(true);
        }

        void closeButtonPressed() override { app.systemRequestedQuit(); }

    private:
        JUCEApplication &app;

        JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(MainWindow)
    };

    MainWindow *mainWindow{nullptr};
    GameView *view{nullptr};
    Agent *red{nullptr};
    Agent *black{nullptr};
    GameModel *model{nullptr};
};

START_JUCE_APPLICATION(Application)