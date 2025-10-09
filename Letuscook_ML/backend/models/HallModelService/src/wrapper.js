// wrapper.js
function calorieAPI(isMale, age, height, initWeight, goalWeight, pal, time) {
    // Baseline ở cân nặng ban đầu
    var baseline = new Baseline(isMale, age, height, initWeight, null, null, pal);

    // 1) Calories để duy trì cân hiện tại (current maintenance)
    var maintainCurrent = baseline.getMaintCals();

    // 2) Calories/ngày để đạt mục tiêu (reach goal)
    //    y hệt UI: dùng Intervention.forgoal tìm mức intake đạt goalWeight sau 'time' ngày
    var minCal = 0.0, eps = 1e-3, actChangePct = 0;
    var goalIntervention = Intervention.forgoal(
        baseline,            // baseline ban đầu
        goalWeight,          // cân nặng mục tiêu
        time,                // số ngày
        actChangePct,        // % thay đổi hoạt động (0 nếu giữ PAL)
        minCal,              // min calories khởi điểm (UI để 0, cảnh báo <1000 hiển thị sau)
        eps
    );
    var reachGoal = goalIntervention.calories;

    // 3) Calories để duy trì ở cân mục tiêu (maintain goal)
    //    UI mô phỏng tới ngày (time + 1) rồi gọi cals4balance
    var goalBody = BodyModel.projectFromBaselineViaIntervention(baseline, goalIntervention, time + 1);
    var maintainGoal = goalBody.cals4balance(baseline, goalIntervention.getAct(baseline));

    return reachGoal;
}
