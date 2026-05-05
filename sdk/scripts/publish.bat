@echo off
echo ========================================
echo   AGI AutoPoster - PyPI 发布脚本
echo ========================================
echo.

echo [1/4] 清理旧的构建文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"
echo 清理完成
echo.

echo [2/4] 安装构建工具（如未安装）...
pip install build twine --quiet
echo 工具准备完成
echo.

echo [3/4] 构建包...
python -m build
echo 构建完成
echo.

echo [4/4] 上传到 PyPI...
echo 请输入您的 PyPI 用户名和密码
python -m twine upload dist/*

echo.
echo ========================================
echo   发布完成！
echo ========================================
pause
