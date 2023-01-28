#pragma once

#include "software/ai/hl/stp/tactic/stop/stop_fsm.h"
#include "software/ai/hl/stp/tactic/tactic.h"

/**
 * The StopTactic will stop the robot from moving. The robot will actively try and brake
 * to come to a halt.
 */
class StopTactic : public Tactic
{
   public:
    /**
     * Creates a new StopTactic
     */
    explicit StopTactic();

    void accept(TacticVisitor& visitor) const override;

    DEFINE_TACTIC_DONE_AND_GET_FSM_STATE

   private:
    void updatePrimitive(const TacticUpdate& tactic_update, bool reset_fsm) override;

    std::map<RobotId, std::unique_ptr<FSM<StopFSM>>> fsm_map;
};
