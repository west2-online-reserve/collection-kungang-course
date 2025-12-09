import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import os
import json
from scipy import signal
from scipy.interpolate import interp1d
from tqdm import tqdm
import matplotlib.pyplot as plt


class AdvancedPullUpBenchmark:
    def __init__(self):
        # MediaPipe初始化
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # 关键点定义
        self.LANDMARK_INDICES = {
            'LEFT_SHOULDER': 11, 'RIGHT_SHOULDER': 12,
            'LEFT_ELBOW': 13, 'RIGHT_ELBOW': 14,
            'LEFT_WRIST': 15, 'RIGHT_WRIST': 16,
            'LEFT_HIP': 23, 'RIGHT_HIP': 24,
            'LEFT_KNEE': 25, 'RIGHT_KNEE': 26,
            'LEFT_ANKLE': 27, 'RIGHT_ANKLE': 28
        }

        self.BENCHMARK_POINTS = [0, 25, 50, 75, 100]

    def extract_comprehensive_landmarks(self, video_path, output_video_path=None):
        """提取关键点数据并生成可视化视频"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"❌ 无法打开视频文件: {video_path}")
            return None

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        print(f"📊 视频信息: {width}x{height}, FPS: {fps}, 总帧数: {total_frames}")

        # 视频写入器
        out = None
        if output_video_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
            print(f"🎬 将生成可视化视频: {output_video_path}")

        # 自定义躯干连接线
        TORSO_CONNECTIONS = [
            (15, 13),   # 手腕-肘部
            (13, 11),   # 肘部-肩膀
            (11, 23), # 肩膀-髋部
            (23, 25), # 髋部-膝盖
            (25, 27)  # 膝盖-脚踝
        ]

        landmarks_data = []

        with tqdm(total=total_frames, desc="提取关键点并生成视频") as pbar:
            for frame_count in range(total_frames):
                success, frame = cap.read()
                if not success:
                    break

                display_frame = frame.copy()
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.pose.process(frame_rgb)

                frame_data = {
                    'frame': frame_count,
                    'timestamp': frame_count / fps if fps > 0 else frame_count
                }

                if results.pose_landmarks:
                    # 绘制骨架
                    self._draw_custom_skeleton(display_frame, results.pose_landmarks, TORSO_CONNECTIONS, width, height)

                    # 保存关键点数据（可选，如果您需要后续分析）
                    for name, idx in self.LANDMARK_INDICES.items():
                        landmark = results.pose_landmarks.landmark[idx]
                        frame_data[f'{name}_X'] = landmark.x
                        frame_data[f'{name}_Y'] = landmark.y
                        frame_data[f'{name}_Z'] = landmark.z
                        frame_data[f'{name}_VIS'] = landmark.visibility

                else:
                    # 即使没有检测到关键点，也标记缺失数据
                    for name in self.LANDMARK_INDICES.keys():
                        frame_data[f'{name}_X'] = np.nan
                        frame_data[f'{name}_Y'] = np.nan
                        frame_data[f'{name}_Z'] = np.nan
                        frame_data[f'{name}_VIS'] = np.nan

                # 保存到视频文件
                if out:
                    out.write(display_frame)

                frame_data.update(self._calculate_upper_stability(results.pose_landmarks))
                frame_data.update(self._calculate_low_stability(results.pose_landmarks))
                frame_data.update(self._calculate_height_metrics(results.pose_landmarks))
                landmarks_data.append(frame_data)
                pbar.update(1)
            else:
                # 即使没有检测到关键点，也保存原始帧到视频
                if out:
                    out.write(display_frame)

                # 标记缺失数据
                frame_data.update(self._get_nan_metrics())

            landmarks_data.append(frame_data)
            pbar.update(1)

        cap.release()
        if out:
            out.release()
        cv2.destroyAllWindows()

        if output_video_path:
            print(f"✅ 可视化视频已保存: {output_video_path}")

        return pd.DataFrame(landmarks_data)

    def _draw_custom_skeleton(self, frame, landmarks, connections, width, height):
        """自定义绘制骨架"""
        # 1. 首先绘制连接线
        for start_idx, end_idx in connections:
            start_landmark = landmarks.landmark[start_idx]
            end_landmark = landmarks.landmark[end_idx]

            # 只绘制可见的关键点之间的连接线
            if start_landmark.visibility > 0.5 and end_landmark.visibility > 0.5:
                start_x = int(start_landmark.x * width)
                start_y = int(start_landmark.y * height)
                end_x = int(end_landmark.x * width)
                end_y = int(end_landmark.y * height)

                # 绘制连接线（黄色，粗细为2）
                cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 255), 2)

        # 2. 绘制关键点
        connected_points = set()
        for connection in connections:
            connected_points.add(connection[0])
            connected_points.add(connection[1])

        for point_idx in connected_points:
            landmark = landmarks.landmark[point_idx]
            if landmark.visibility > 0.5:  # 只绘制可见的关键点
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                # 绘制关键点（绿色圆点，半径为5）
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                # 添加白色边框
                cv2.circle(frame, (x, y), 6, (255, 255, 255), 1)

    def _get_landmark_point(self, landmarks, idx, width, height):
        """获取关键点像素坐标"""
        landmark = landmarks.landmark[idx]
        return (int(landmark.x * width), int(landmark.y * height))

    def _calculate_upper_stability(self,landmarks):
        metrics={}
        try:
            left_shoulder = np.array([landmarks.landmark[11].x, landmarks.landmark[11].y])
            left_hip = np.array([landmarks.landmark[23].x, landmarks.landmark[23].y])

            # 躯干向量
            dx = left_shoulder[0] - left_hip[0]  # 水平分量
            dy = left_shoulder[1] - left_hip[1]  # 垂直分量

            # 计算与垂直线的夹角
            angle = np.degrees(np.arctan2(dx, dy))
            metrics['TORSO_ANGLE_side'] = angle
            metrics['TORSO_ANGLE_ABS_side'] = abs(angle)  # 绝对值表示倾斜程度

        except Exception as e:
            metrics['TORSO_ANGLE'] = np.nan
            metrics['TORSO_ANGLE_ABS'] = np.nan

        return metrics

    def _calculate_low_stability(self,landmarks):
        metrics={}
        try:
            left_knee = np.array([landmarks.landmark[25].x, landmarks.landmark[25].y])
            left_hip = np.array([landmarks.landmark[23].x, landmarks.landmark[23].y])

            # 躯干向量
            dx = left_hip[0] - left_knee[0]  # 水平分量
            dy = left_hip[1] - left_knee[1]  # 垂直分量

            # 计算与垂直线的夹角
            angle = np.degrees(np.arctan2(dx, dy))
            metrics['LOWER_ANGLE_side'] = angle
            metrics['LOWER_ANGLE_ABS_side'] = abs(angle)  # 绝对值表示倾斜程度

        except Exception as e:
            metrics['LOWER_ANGLE_side'] = np.nan
            metrics['LOWER_ANGLE_ABS_side'] = np.nan

        return metrics


    def _calculate_height_metrics(self, landmarks):
        """计算高度相关指标"""
        metrics = {}
        try:
            # 使用归一化坐标（0-1范围）
            left_wrist_y = landmarks.landmark[15].y
            left_shoulder_y = landmarks.landmark[11].y

            metrics['LEFT_WRIST_Y'] = left_wrist_y
            metrics['LEFT_SHOULDER_Y'] = left_shoulder_y
        except Exception as e:
            metrics.update({key: np.nan for key in [
                'LEFT_WRIST_Y', 'LEFT_SHOULDER_Y',
            ]})

        return metrics

    def detect_rep_cycles_by_shoulder_height(self, df):
        """基于肩膀高度检测引体向上周期"""
        print("基于肩膀高度检测引体向上周期...")

        # 使用肩膀高度作为主要信号
        shoulder_heights = df['LEFT_SHOULDER_Y'].values

        # 数据清理和插值
        shoulder_series = pd.Series(shoulder_heights)
        shoulder_interp = shoulder_series.interpolate(method='linear', limit_direction='both')

        if len(shoulder_interp) < 20:
            print("数据太少，无法检测周期")
            return []

        # 平滑信号
        window_size = min(11, len(shoulder_interp) // 10 * 2 + 1)
        if window_size < 3:
            window_size = 3

        try:
            smoothed = signal.savgol_filter(shoulder_interp, window_length=window_size, polyorder=2)
        except Exception as e:
            print(f"平滑信号失败: {e}")
            smoothed = shoulder_interp.values

        # 寻找周期
        rep_cycles = self._find_cycles_by_shoulder_height(smoothed)
        print(f"检测到 {len(rep_cycles)} 个引体向上周期")
        return rep_cycles

    def _find_cycles_by_shoulder_height(self, shoulder_heights):
        """基于肩膀高度寻找周期"""
        rep_cycles = []

        try:
            min_distance = max(15, len(shoulder_heights) // 20)

            # 寻找波谷（肩膀最高点）
            valleys, _ = signal.find_peaks(-shoulder_heights, distance=min_distance, prominence=0.02)
            # 寻找波峰（肩膀最低点）
            peaks, _ = signal.find_peaks(shoulder_heights, distance=min_distance, prominence=0.02)

            print(f"肩膀高度检测: {len(peaks)}个波峰(手臂伸直), {len(valleys)}个波谷(下巴过杆)")

            # 构建周期
            if len(peaks) >= 2 and len(valleys) >= 1:
                for i in range(len(peaks) - 1):
                    start_peak = peaks[i]
                    end_peak = peaks[i + 1]

                    # 在两个波峰之间寻找波谷
                    valleys_between = [v for v in valleys if start_peak < v < end_peak]

                    if valleys_between:
                        valley = valleys_between[0]

                        if self._validate_rep_cycle(shoulder_heights, start_peak, valley, end_peak):
                            rep_cycles.append({
                                'start_frame': int(start_peak),
                                'bottom_frame': int(valley),
                                'end_frame': int(end_peak),
                                'duration': int(end_peak - start_peak),
                                'amplitude': float(shoulder_heights[start_peak] - shoulder_heights[valley])
                            })

        except Exception as e:
            print(f"肩膀高度周期检测错误: {e}")

        return rep_cycles

    def _validate_rep_cycle(self, signal_data, start, bottom, end):
        """验证周期有效性"""
        try:
            if end <= start or bottom <= start or end <= bottom:
                return False

            duration = end - start
            amplitude = signal_data[start] - signal_data[bottom]

            # 宽松的验证条件
            if duration < 10 or duration > 200 or amplitude < 0.02:
                return False

            return True
        except Exception as e:
            return False

    def create_biomechanical_benchmark(self, df, rep_cycles):
        """创建生物力学基准"""
        if not rep_cycles:
            print("没有检测到周期，创建空基准")
            return self._create_empty_benchmark()

        # 分析每个周期
        cycle_analyses = {}

        for i, cycle in enumerate(rep_cycles):
            cycle_name = f"cycle_{i + 1}"
            cycle_analysis = self._analyze_single_cycle(df, cycle, cycle_name)
            if cycle_analysis:
                cycle_analyses[cycle_name] = cycle_analysis

        if not cycle_analyses:
            return self._create_empty_benchmark()

        # 创建基准结果
        benchmark = {
            'analysis_summary': {
                'total_cycles': len(cycle_analyses),
                'total_frames': len(df),
                'analysis_timestamp': pd.Timestamp.now().isoformat(),
                'status': 'success'
            },
            'cycles': cycle_analyses
        }

        return benchmark

    def _analyze_single_cycle(self, df, cycle, cycle_name):
        """分析单个周期"""
        try:
            start, bottom, end = cycle['start_frame'], cycle['bottom_frame'], cycle['end_frame']

            if end >= len(df):
                return None

            cycle_data = df.iloc[start:end].copy()


            # 计算上半身躯干角度统计
            torso_angles = cycle_data['TORSO_ANGLE_ABS_side'].dropna()
            torso_stats = {
                '侧面_torso_angle_max': float(np.max(torso_angles)) if len(torso_angles) > 0 else np.nan,
                '侧面_torso_angle_min': float(np.min(torso_angles)) if len(torso_angles) > 0 else np.nan,
                '侧面_torso_angle_mean': float(np.mean(torso_angles)) if len(torso_angles) > 0 else np.nan,
                '侧面_torso_angle_std': float(np.std(torso_angles)) if len(torso_angles) > 0 else np.nan
            }

            low_angles = cycle_data['LOWER_ANGLE_ABS_side'].dropna()
            low_stats = {
                '侧面_low_angle_max': float(np.max(low_angles)) if len(low_angles) > 0 else np.nan,
                '侧面_low_angle_min': float(np.min(low_angles)) if len(low_angles) > 0 else np.nan,
                '侧面_low_angle_mean': float(np.mean(low_angles)) if len(low_angles) > 0 else np.nan,
                '侧面_low_angle_std': float(np.std(low_angles)) if len(low_angles) > 0 else np.nan
            }

            cycle_analysis = {
                'cycle_info': {
                    'start_frame': int(start),
                    'bottom_frame': int(bottom),
                    'end_frame': int(end),
                    'duration_frames': int(end - start),
                    'amplitude': float(cycle['amplitude'])
                },
                'torso_metrics': torso_stats,
                'low_metrics': low_stats
            }

            return cycle_analysis

        except Exception as e:
            print(f"分析周期 {cycle_name} 错误: {e}")
            return None
    def _get_nan_metrics(self):
        """返回NaN指标字典"""
        return {
            'LEFT_SHOULDER_Y': np.nan,
        }

    def _create_empty_benchmark(self):
        """创建空基准"""
        return {
            'analysis_summary': {
                'total_cycles': 0,
                'total_frames': 0,
                'analysis_timestamp': pd.Timestamp.now().isoformat(),
                'status': 'no_cycles_detected'
            },
            'cycles': {}
        }

def process(side_path):
    benchmark_system = AdvancedPullUpBenchmark()
    df = benchmark_system.extract_comprehensive_landmarks(side_path)
    i=0
    if df is not None:
        rep_cycles = benchmark_system.detect_rep_cycles_by_shoulder_height(df)
        # 创建基准
        benchmark = benchmark_system.create_biomechanical_benchmark(df, rep_cycles)
        # 打印结果摘要
        if benchmark['analysis_summary']['status'] == 'success':
            res='从侧面看的周期分析：'
            for cycle_name, cycle_data in benchmark['cycles'].items():
                # print(f"\n{cycle_name}:")
                i=i+1
                upper = cycle_data['torso_metrics']
                low = cycle_data['low_metrics']
                res+=(f"第{i}个周期：我的肩膀与髋部连线与竖直线的角度为：最大={upper['侧面_torso_angle_max']:.1f}°, "
                      f"最小={upper['侧面_torso_angle_min']:.1f}°, 平均={upper['侧面_torso_angle_mean']:.1f}°;"
                      f"我的大腿与竖直线的角度为：最大={low['侧面_low_angle_max']:.1f}°,"
                      f"最小={low['侧面_low_angle_min']:.1f}°, 平均={low['侧面_low_angle_mean']:.1f}。")
            return res
        else:
            print("❌ 未检测到有效的引体向上周期")
            return None
    else:
        print("❌ 数据提取失败")
        return None
