import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import json
from scipy import signal
from tqdm import tqdm


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
            'LEFT_KNEE': 25, 'RIGHT_KNEE': 26
        }

        self.BENCHMARK_POINTS = [0, 25, 50, 75, 100]

    def extract_comprehensive_landmarks(self, video_path, output_video_path=None):
        """提取综合关键点数据并生成简单可视化视频"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # 视频写入器
        out = None
        if output_video_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
            print(f"🎬 将生成可视化视频: {output_video_path}")

        # 自定义躯干连接线
        TORSO_CONNECTIONS = [
            (15, 13), (16, 14), (13, 11), (14, 12),
            (11, 12), (11, 23), (12, 24), (23, 24),
            (23, 25), (24, 26), (25, 27), (26, 28)
        ]

        landmarks_data = []

        with tqdm(total=total_frames, desc="提取综合关键点") as pbar:
            for frame_count in range(total_frames):
                success, frame = cap.read()
                if not success:
                    break

                display_frame = frame.copy()
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.pose.process(frame_rgb)

                frame_data = {
                    'frame': frame_count,
                    'timestamp': frame_count / fps
                }

                if results.pose_landmarks:
                    # 绘制骨架
                    self._draw_custom_skeleton(display_frame, results.pose_landmarks, TORSO_CONNECTIONS, width, height)

                    # 保存到视频文件
                    if out:
                        out.write(display_frame)

                    # 计算所有指标
                    frame_data.update(self._calculate_grip_metrics(results.pose_landmarks))
                    frame_data.update(self._calculate_height_metrics(results.pose_landmarks))
                    frame_data.update(self._calculate_torso_angle(results.pose_landmarks))

                else:
                    # 即使没有检测到关键点，也保存原始帧到视频
                    if out:
                        out.write(display_frame)

                    # 标记缺失数据
                    frame_data.update(self._get_nan_metrics())

                landmarks_data.append(frame_data)
                pbar.update(1)

        cap.release()

        # 关闭视频写入器
        if out:
            out.release()
            print(f"✅ 可视化视频已保存: {output_video_path}")

        return pd.DataFrame(landmarks_data)

    def _calculate_grip_metrics(self, landmarks):
        """计算握距相关指标"""
        metrics = {}
        try:
            # 使用世界坐标计算握距
            left_wrist = np.array([landmarks.landmark[15].x, landmarks.landmark[15].y])
            right_wrist = np.array([landmarks.landmark[16].x, landmarks.landmark[16].y])
            left_shoulder = np.array([landmarks.landmark[11].x, landmarks.landmark[11].y])
            right_shoulder = np.array([landmarks.landmark[12].x, landmarks.landmark[12].y])

            wrist_distance = np.linalg.norm(left_wrist - right_wrist)
            shoulder_distance = np.linalg.norm(left_shoulder - right_shoulder)

            metrics['GRIP_WIDTH'] = wrist_distance
            metrics['SHOULDER_WIDTH'] = shoulder_distance
            metrics['GRIP_RATIO'] = wrist_distance / shoulder_distance if shoulder_distance > 0 else np.nan

        except Exception as e:
            metrics['GRIP_WIDTH'] = np.nan
            metrics['SHOULDER_WIDTH'] = np.nan
            metrics['GRIP_RATIO'] = np.nan

        return metrics

    def _calculate_height_metrics(self, landmarks):
        """计算高度相关指标"""
        metrics = {}
        try:
            # 使用归一化坐标（0-1范围）
            left_wrist_y = landmarks.landmark[15].y
            right_wrist_y = landmarks.landmark[16].y
            left_shoulder_y = landmarks.landmark[11].y
            right_shoulder_y = landmarks.landmark[12].y

            metrics['LEFT_WRIST_Y'] = left_wrist_y
            metrics['RIGHT_WRIST_Y'] = right_wrist_y
            metrics['LEFT_SHOULDER_Y'] = left_shoulder_y
            metrics['RIGHT_SHOULDER_Y'] = right_shoulder_y
            metrics['AVG_WRIST_HEIGHT'] = (left_wrist_y + right_wrist_y) / 2
            metrics['AVG_SHOULDER_HEIGHT'] = (left_shoulder_y + right_shoulder_y) / 2
            metrics['MIN_SHOULDER_HEIGHT'] = min(left_shoulder_y, right_shoulder_y)

        except Exception as e:
            metrics.update({key: np.nan for key in [
                'LEFT_WRIST_Y', 'RIGHT_WRIST_Y', 'LEFT_SHOULDER_Y', 'RIGHT_SHOULDER_Y',
                'AVG_WRIST_HEIGHT', 'AVG_SHOULDER_HEIGHT', 'MIN_SHOULDER_HEIGHT'
            ]})

        return metrics

    def _calculate_torso_angle(self, landmarks):
        """计算躯干角度"""
        metrics = {}
        try:
            # 肩膀中心
            left_shoulder = np.array([landmarks.landmark[11].x, landmarks.landmark[11].y])
            right_shoulder = np.array([landmarks.landmark[12].x, landmarks.landmark[12].y])
            shoulder_center = (
                (left_shoulder[0] + right_shoulder[0]) / 2,
                (left_shoulder[1] + right_shoulder[1]) / 2
            )

            # 髋部中心
            left_hip = np.array([landmarks.landmark[23].x, landmarks.landmark[23].y])
            right_hip = np.array([landmarks.landmark[24].x, landmarks.landmark[24].y])
            hip_center = (
                (left_hip[0] + right_hip[0]) / 2,
                (left_hip[1] + right_hip[1]) / 2
            )

            # 躯干向量
            dx = shoulder_center[0] - hip_center[0]  # 水平分量
            dy = shoulder_center[1] - hip_center[1]  # 垂直分量

            # 计算与垂直线的夹角
            angle = np.degrees(np.arctan2(dx, dy))
            metrics['TORSO_ANGLE'] = angle
            metrics['TORSO_ANGLE_ABS'] = abs(angle)  # 绝对值表示倾斜程度

        except Exception as e:
            metrics['TORSO_ANGLE'] = np.nan
            metrics['TORSO_ANGLE_ABS'] = np.nan

        return metrics

    def _draw_custom_skeleton(self, frame, landmarks, connections, width, height):
        """自定义绘制骨架"""
        # 绘制连接线
        for start_idx, end_idx in connections:
            start_landmark = landmarks.landmark[start_idx]
            end_landmark = landmarks.landmark[end_idx]

            if start_landmark.visibility > 0.5 and end_landmark.visibility > 0.5:
                start_x = int(start_landmark.x * width)
                start_y = int(start_landmark.y * height)
                end_x = int(end_landmark.x * width)
                end_y = int(end_landmark.y * height)

                cv2.line(frame, (start_x, start_y), (end_x, end_y), (0, 255, 255), 2)

        # 绘制关键点
        connected_points = set()
        for connection in connections:
            connected_points.add(connection[0])
            connected_points.add(connection[1])

        for point_idx in connected_points:
            landmark = landmarks.landmark[point_idx]
            if landmark.visibility > 0.5:
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    def detect_rep_cycles_by_shoulder_height(self, df):
        """基于肩膀高度检测引体向上周期"""
        print("基于肩膀高度检测引体向上周期...")

        # 使用肩膀高度作为主要信号
        shoulder_heights = df['MIN_SHOULDER_HEIGHT'].values

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
            peaks = self._add_boundary_peaks(shoulder_heights, peaks, min_distance)
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

    def _add_boundary_peaks(self, signal_data, detected_peaks, min_distance):
        peaks = list(detected_peaks)

        # 检查起始边界（第一帧）
        if len(signal_data) > 0:
            search_range = min(min_distance, len(signal_data) // 4)
            if search_range > 0:
                first_value = signal_data[0]  # 第一帧的值
                subsequent_values = signal_data[1:search_range]  # 后续几帧

                # 条件1：第一帧 > 后续帧的最大值
                if len(subsequent_values) > 0 and first_value > np.max(subsequent_values):
                    # 条件2：第一帧 > 整个数据的60%分位数（确保是真正的高点）
                    if first_value > np.percentile(signal_data, 60):
                        peaks.insert(0, 0)  # 添加第一帧为波峰

        return np.array(sorted(peaks))

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

            # 计算握距统计
            grip_ratios = cycle_data['GRIP_RATIO'].dropna()
            grip_stats = {
                'grip_ratio_mean': float(np.mean(grip_ratios)) if len(grip_ratios) > 0 else np.nan,
                'grip_ratio_max': float(np.max(grip_ratios)) if len(grip_ratios) > 0 else np.nan,
                'grip_ratio_min': float(np.min(grip_ratios)) if len(grip_ratios) > 0 else np.nan,
                'grip_ratio_std': float(np.std(grip_ratios)) if len(grip_ratios) > 0 else np.nan
            }

            # 计算躯干角度统计
            torso_angles = cycle_data['TORSO_ANGLE_ABS'].dropna()
            torso_stats = {
                'torso_angle_max': float(np.max(torso_angles)) if len(torso_angles) > 0 else np.nan,
                'torso_angle_min': float(np.min(torso_angles)) if len(torso_angles) > 0 else np.nan,
                'torso_angle_mean': float(np.mean(torso_angles)) if len(torso_angles) > 0 else np.nan,
                'torso_angle_std': float(np.std(torso_angles)) if len(torso_angles) > 0 else np.nan
            }

            # 计算最高点（下巴过杠点）的肩膀中心与手腕中心高度差
            peak_height_diff = self._calculate_peak_height_difference(cycle_data, bottom)

            cycle_analysis = {
                'cycle_info': {
                    'start_frame': int(start),
                    'bottom_frame': int(bottom),
                    'end_frame': int(end),
                    'duration_frames': int(end - start),
                    'amplitude': float(cycle['amplitude'])
                },
                'grip_metrics': grip_stats,
                'torso_metrics': torso_stats,
                'peak_height_difference': peak_height_diff
            }

            return cycle_analysis

        except Exception as e:
            print(f"分析周期 {cycle_name} 错误: {e}")
            return None

    def _calculate_peak_height_difference(self, cycle_data, bottom_frame):
        """计算最高点（下巴过杠点）的肩膀中心与手腕中心高度差"""
        try:
            # 修正索引处理：找到cycle_data中距离bottom_frame最近的帧
            cycle_start = cycle_data.index[0]
            relative_bottom = bottom_frame - cycle_start

            # 确保索引在有效范围内
            if 0 <= relative_bottom < len(cycle_data):
                bottom_data = cycle_data.iloc[relative_bottom]

                # 获取高度数据
                shoulder_center_y = bottom_data.get('AVG_SHOULDER_HEIGHT', np.nan)
                wrist_center_y = bottom_data.get('AVG_WRIST_HEIGHT', np.nan)

                # print(f"调试: 帧{bottom_frame} - 肩膀高度: {shoulder_center_y}, 手腕高度: {wrist_center_y}")  # 调试信息

                if not np.isnan(shoulder_center_y) and not np.isnan(wrist_center_y):
                    height_diff = shoulder_center_y - wrist_center_y
                    return {
                        'height_difference': float(height_diff),
                        'shoulder_height': float(shoulder_center_y),
                        'wrist_height': float(wrist_center_y),
                        'frame': int(bottom_frame)
                    }

            return {
                'height_difference': np.nan,
                'shoulder_height': np.nan,
                'wrist_height': np.nan,
                'frame': int(bottom_frame)
            }

        except Exception as e:
            print(f"计算高度差错误: {e}")
            return {
                'height_difference': np.nan,
                'shoulder_height': np.nan,
                'wrist_height': np.nan,
                'frame': int(bottom_frame)
            }

    def _get_nan_metrics(self):
        """返回NaN指标字典"""
        return {
            'GRIP_WIDTH': np.nan, 'SHOULDER_WIDTH': np.nan, 'GRIP_RATIO': np.nan,
            'LEFT_WRIST_Y': np.nan, 'RIGHT_WRIST_Y': np.nan,
            'LEFT_SHOULDER_Y': np.nan, 'RIGHT_SHOULDER_Y': np.nan,
            'AVG_WRIST_HEIGHT': np.nan, 'AVG_SHOULDER_HEIGHT': np.nan, 'MIN_SHOULDER_HEIGHT': np.nan,
            'WRIST_SHOULDER_DIFF_LEFT': np.nan, 'WRIST_SHOULDER_DIFF_RIGHT': np.nan, 'WRIST_SHOULDER_DIFF_AVG': np.nan,
            'TORSO_ANGLE': np.nan, 'TORSO_ANGLE_ABS': np.nan
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



def process(front_path):
    benchmark_system = AdvancedPullUpBenchmark()
    i = 0

    df = benchmark_system.extract_comprehensive_landmarks(front_path)
    if df is not None:
        # 检测周期
        rep_cycles = benchmark_system.detect_rep_cycles_by_shoulder_height(df)
        # print(f"✅ 检测到 {len(rep_cycles)} 个周期")
        # 创建基准
        benchmark = benchmark_system.create_biomechanical_benchmark(df, rep_cycles)
        # 打印结果摘要
        if benchmark['analysis_summary']['status'] == 'success':
            res=f'我一共做了{len(rep_cycles)}个引体向上,下面是我每个周期从正面看的描述：'
            # print(f"\n📊 分析摘要:")
            # print(f"   周期数: {benchmark['analysis_summary']['total_cycles']}")

            for cycle_name, cycle_data in benchmark['cycles'].items():
                i = i + 1
                print(f"\n{cycle_name}:")
                grip = cycle_data['grip_metrics']
                torso = cycle_data['torso_metrics']
                peak = cycle_data['peak_height_difference']

                res=res+(f"第{i}个周期：我的握距相对肩宽比例为：平均={grip['grip_ratio_mean']:.3f},最大={grip['grip_ratio_max']:.3f}, "
                         f"最小={grip['grip_ratio_min']:.3f} ;我的脊柱相对竖直线角度为：最大={torso['torso_angle_max']:.1f}°,"
                         f"最小={torso['torso_angle_min']:.1f}°, 平均={torso['torso_angle_mean']:.1f}°"
                         f"在最高点时，我肩膀连线与手腕连线的高度差为{peak['height_difference']:.3f}(这里为像素距离，我以此判断有没有过杆)。")


            return res,len(rep_cycles)
        else:
            print("❌ 未检测到有效的引体向上周期")
            return None
    else:
        print("❌ 数据提取失败")
        return None

if __name__ == '__main__':

    print(process('./4.mp4'))
