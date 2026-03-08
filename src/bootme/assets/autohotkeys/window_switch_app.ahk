!`:: {
    static lastExe := ""
    static windowList := []
    static currentIndex := 0

    ; 获取当前活动窗口信息
    try {
        activeHwnd := WinExist("A")
        activeExe := WinGetProcessName("ahk_id " activeHwnd)
    } catch {
        return ; 避免在特殊窗口下报错
    }

    ; 如果切换了应用，或者窗口数量发生了变化，则更新缓存列表
    currentWindows := WinGetList("ahk_exe " activeExe)
    
    if (activeExe != lastExe || currentWindows.Length != windowList.Length) {
        windowList := currentWindows
        lastExe := activeExe
        currentIndex := 1
        
        ; 找到当前窗口在列表中的初始位置
        for i, id in windowList {
            if (id == activeHwnd) {
                currentIndex := i
                break
            }
        }
    }

    ; 计算下一个索引
    currentIndex += 1
    if (currentIndex > windowList.Length) {
        currentIndex := 1
    }

    ; 激活目标窗口
    targetHwnd := windowList[currentIndex]
    if WinExist("ahk_id " targetHwnd) {
        WinActivate("ahk_id " targetHwnd)
    }
}
