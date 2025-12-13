import unittest
from datetime import datetime

# 假设上面的代码保存在 database_driver.py 中
from opengauss import DatabaseConfig, ClassManagementSystem


class TestDatabaseDriver(unittest.TestCase):
    """数据库驱动库测试类"""

    @classmethod
    def setUpClass(cls):
        """测试前设置数据库配置"""
        # 这里使用测试数据库配置，请根据实际情况修改
        cls.test_config = DatabaseConfig(
            host="localhost",
            user="gaussdb",  # 测试用户
            password="openGauss@123",  # 测试密码
            database="postgres",  # 测试数据库
            port="5432"
        )

        cls.system = ClassManagementSystem(cls.test_config)

    def setUp(self):
        """每个测试用例前的准备工作"""
        # 初始化数据库表
        self.system.initialize()

        # 清理可能存在的测试数据
        self._cleanup_test_data()

    def tearDown(self):
        """每个测试用例后的清理工作"""
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """清理测试数据"""
        conn = self.system.db_connection.get_connection()
        try:
            with conn.cursor() as cursor:
                # 注意：由于外键约束，需要按顺序删除
                cursor.execute("DELETE FROM history_records")
                cursor.execute("DELETE FROM login_records")
                cursor.execute("DELETE FROM training_plans")
                cursor.execute("DELETE FROM feedback")
                cursor.execute("DELETE FROM video_records")
                cursor.execute("DELETE FROM ratings")
                cursor.execute("DELETE FROM users")
            conn.commit()
        except Exception as e:
            print(f"清理测试数据失败: {e}")
            conn.rollback()

    def test_01_initialize_database(self):
        """测试数据库初始化"""
        result = self.system.initialize()
        self.assertTrue(result, "数据库初始化失败")

    def test_02_user_operations(self):
        """测试用户管理操作"""
        user_manager = self.system.user_manager

        # 测试添加用户
        result = user_manager.add_user(
            username="test_user",
            password="test_password",
            height=175.5,
            weight=70.0,
            role="user"
        )
        self.assertTrue(result, "添加用户失败")

        # 测试查询用户
        user = user_manager.get_user_by_username("test_user")
        self.assertIsNotNone(user, "查询用户失败")
        self.assertEqual(user['username'], "test_user")
        self.assertEqual(float(user['height']), 175.5)
        self.assertEqual(float(user['weight']), 70.0)

        # 测试更新用户
        user_id = user['id']
        update_result = user_manager.update_user(
            userid=user_id,
            username="updated_user",
            weight=72.5
        )
        self.assertTrue(update_result, "更新用户失败")

        # 验证更新
        updated_user = user_manager.get_user_by_username("updated_user")
        self.assertIsNotNone(updated_user)
        self.assertEqual(float(updated_user['weight']), 72.5)

        # 测试获取所有用户
        all_users = user_manager.get_all_users()
        self.assertGreaterEqual(len(all_users), 1)

    def test_03_login_operations(self):
        """测试登录记录操作"""
        user_manager = self.system.user_manager
        login_manager = self.system.login_manager

        # 先创建用户
        user_manager.add_user("login_test_user", "password")
        user = user_manager.get_user_by_username("login_test_user")
        user_id = user['id']

        # 测试添加登录记录
        result = login_manager.add_login_record(user_id)
        self.assertTrue(result, "添加登录记录失败")

        # 测试查询用户登录记录
        user_logins = login_manager.get_login_records_by_user(user_id)
        self.assertGreaterEqual(len(user_logins), 1)

        # 测试获取所有登录记录
        all_logins = login_manager.get_all_login_records()
        self.assertGreaterEqual(len(all_logins), 1)


    def test_06_training_plan_operations(self):
        """测试训练计划操作"""
        user_manager = self.system.user_manager
        training_plan_manager = self.system.training_plan_manager

        # 创建测试用户
        user_manager.add_user("plan_test_user", "password")
        user = user_manager.get_user_by_username("plan_test_user")
        user_id = user['id']

        # 测试添加训练计划
        plan_id = training_plan_manager.add_training_plan(
            user_id=user_id,
            date=datetime.now(),
            project="俯卧撑",
            target=50,
            note="每天训练"
        )
        self.assertNotEqual(plan_id, -1, "添加训练计划失败")

        # 测试查询用户训练计划
        user_plans = training_plan_manager.get_user_plans(user_id)
        self.assertGreaterEqual(len(user_plans), 1)
        self.assertEqual(user_plans[0]['project'], "俯卧撑")
        self.assertEqual(user_plans[0]['target'], 50)

        # 测试查询特定训练计划
        plan = training_plan_manager.get_plan_by_id(plan_id)
        self.assertIsNotNone(plan, "查询训练计划失败")

        # 测试更新训练计划
        update_result = training_plan_manager.update_training_plan(
            plan_id=plan_id,
            user_id=user_id,
            target=60,
            completed=True,
            actualCount=55
        )
        self.assertTrue(update_result, "更新训练计划失败")

        # 验证更新
        updated_plan = training_plan_manager.get_plan_by_id(plan_id)
        self.assertEqual(updated_plan['target'], 60)
        self.assertTrue(updated_plan['completed'])
        self.assertEqual(updated_plan['actualcount'], 55)

        # 测试删除训练计划
        delete_result = training_plan_manager.delete_training_plan(plan_id, user_id)
        self.assertTrue(delete_result, "删除训练计划失败")

        # 验证删除
        deleted_plan = training_plan_manager.get_plan_by_id(plan_id)
        self.assertIsNone(deleted_plan)

    def test_07_feedback_operations(self):
        """测试反馈操作"""
        user_manager = self.system.user_manager
        feedback_manager = self.system.feedback_manager

        # 创建测试用户
        user_manager.add_user("feedback_test_user", "password")
        user = user_manager.get_user_by_username("feedback_test_user")
        user_id = user['id']

        # 测试添加反馈
        feedback_id = feedback_manager.add_feedback(
            user_id=user_id,
            content="系统很好用",
            email="test@example.com"
        )
        self.assertNotEqual(feedback_id, -1, "添加反馈失败")

        # 测试通过ID查询反馈
        feedback = feedback_manager.get_feedback_by_id(feedback_id)
        self.assertIsNotNone(feedback, "查询反馈失败")
        self.assertEqual(feedback['content'], "系统很好用")
        self.assertEqual(feedback['email'], "test@example.com")

        # 测试获取所有反馈
        all_feedback = feedback_manager.get_all_feedback()
        self.assertGreaterEqual(len(all_feedback), 1)

    def test_08_video_operations(self):
        """测试视频操作"""
        video_manager = self.system.video_manager

        # 测试添加视频
        video_id = video_manager.add_video(
            name="训练教程",
            annotation="引体向上训练方法",
            size=1024000,  # 1MB
            url="http://example.com/video.mp4",
            duration=120.5,
            thumbnail="http://example.com/thumbnail.jpg"
        )
        self.assertNotEqual(video_id, -1, "添加视频失败")

        # 测试获取所有视频
        all_videos = video_manager.get_all_video_records()
        self.assertGreaterEqual(len(all_videos), 1)
        self.assertEqual(all_videos[0]['title'], "训练教程")
        self.assertEqual(all_videos[0]['annotation'], "引体向上训练方法")

    def test_09_trained_date_query(self):
        """测试训练日期查询"""
        user_manager = self.system.user_manager
        training_plan_manager = self.system.training_plan_manager

        # 创建测试用户
        user_manager.add_user("date_test_user", "password")
        user = user_manager.get_user_by_username("date_test_user")
        user_id = user['id']

        # 添加训练计划
        from datetime import datetime, timedelta
        today = datetime.now()
        yesterday = today - timedelta(days=1)

        training_plan_manager.add_training_plan(
            user_id=user_id,
            date=today,
            project="俯卧撑",
            target=50,
            note="今天"
        )

        training_plan_manager.add_training_plan(
            user_id=user_id,
            date=yesterday,
            project="引体向上",
            target=30,
            note="昨天"
        )

        # 测试查询所有训练日期
        dates = training_plan_manager.get_trained_date(user_id)
        self.assertGreaterEqual(len(dates), 2)

        # 测试按年份查询
        current_year = today.year
        dates_this_year = training_plan_manager.get_trained_date(
            user_id=user_id,
            year=current_year
        )
        self.assertGreaterEqual(len(dates_this_year), 2)

        # 测试按年月查询
        current_month = today.month
        dates_this_month = training_plan_manager.get_trained_date(
            user_id=user_id,
            year=current_year,
            month=current_month
        )
        self.assertGreaterEqual(len(dates_this_month), 1)

    def test_10_integration_test(self):
        """测试完整流程集成"""
        # 1. 创建用户
        user_result = self.system.user_manager.add_user(
            username="integration_user",
            password="integration_pass",
            height=180,
            weight=75
        )
        self.assertTrue(user_result)

        # 2. 用户登录
        user = self.system.user_manager.get_user_by_username("integration_user")
        login_result = self.system.login_manager.add_login_record(user['id'])
        self.assertTrue(login_result)

        # 3. 创建评分
        rating_id = self.system.rating_manager.add_rating(
            score=90.0,
            content="综合表现良好"
        )
        self.assertNotEqual(rating_id, -1)

        # 4. 创建历史记录
        history_result = self.system.history_manager.add_history_record(
            user_id=user['id'],
            rating_id=rating_id,
            project="综合训练"
        )
        self.assertTrue(history_result)

        # 5. 创建训练计划
        plan_id = self.system.training_plan_manager.add_training_plan(
            user_id=user['id'],
            date=datetime.now(),
            project="每日训练",
            target=100,
            note="坚持训练"
        )
        self.assertNotEqual(plan_id, -1)

        # 6. 提交反馈
        feedback_id = self.system.feedback_manager.add_feedback(
            user_id=user['id'],
            content="系统非常好用",
            email="user@example.com"
        )
        self.assertNotEqual(feedback_id, -1)

        # 验证数据完整性
        user_logins = self.system.login_manager.get_login_records_by_user(user['id'])
        self.assertEqual(len(user_logins), 1)

        user_history = self.system.history_manager.get_history_by_user(user['id'])
        self.assertEqual(len(user_history), 1)

        user_plans = self.system.training_plan_manager.get_user_plans(user['id'])
        self.assertEqual(len(user_plans), 1)

        user_feedback = self.system.feedback_manager.get_feedback_by_id(feedback_id)
        self.assertIsNotNone(user_feedback)


# 运行测试的函数
def run_tests():
    """运行所有测试"""
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDatabaseDriver)

    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 打印测试结果摘要
    print("\n" + "=" * 50)
    print("测试结果摘要:")
    print(f"运行测试数: {result.testsRun}")
    print(f"失败数: {len(result.failures)}")
    print(f"错误数: {len(result.errors)}")
    print(f"跳过数: {len(result.skipped)}")

    if result.wasSuccessful():
        print("所有测试通过!")
    else:
        print("有测试失败!")

        # 打印失败详情
        for test, traceback in result.failures:
            print(f"\n失败测试: {test}")
            print(f"失败详情:\n{traceback}")

        for test, traceback in result.errors:
            print(f"\n错误测试: {test}")
            print(f"错误详情:\n{traceback}")

    return result.wasSuccessful()


# 快速测试函数（不运行完整单元测试）
def quick_test():
    """快速测试数据库连接和基本功能"""
    print("开始快速测试...")

    # 使用测试数据库配置（请修改为你的配置）
    config = DatabaseConfig(
        host="localhost",
        user="your_user",
        password="your_password",
        database="your_database",
        port="5432"
    )

    system = ClassManagementSystem(config)

    try:
        # 测试连接和初始化
        print("1. 测试数据库连接和初始化...")
        if system.initialize():
            print("   数据库初始化成功")
        else:
            print("   数据库初始化失败")
            return False

        # 测试用户管理
        print("2. 测试用户管理...")
        user_manager = system.user_manager

        # 添加用户
        if user_manager.add_user("quick_test_user", "password", 170, 65):
            print("   添加用户成功")
        else:
            print("   添加用户失败")
            return False

        # 查询用户
        user = user_manager.get_user_by_username("quick_test_user")
        if user:
            print(f"   查询用户成功: ID={user['id']}, 用户名={user['username']}")
        else:
            print("   查询用户失败")
            return False

        # 清理测试数据
        print("3. 清理测试数据...")
        conn = system.db_connection.get_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username LIKE 'test_%' OR username LIKE 'quick_%'")
        conn.commit()
        print("   清理完成")

        # 关闭连接
        system.db_connection.close()
        print("4. 数据库连接已关闭")

        print("\n快速测试通过!")
        return True

    except Exception as e:
        print(f"测试失败: {e}")
        return False


if __name__ == "__main__":
    print("数据库驱动库测试")
    print("=" * 50)

    # 选项：运行完整测试或快速测试
    choice = input("请选择测试方式:\n1. 运行完整单元测试\n2. 运行快速测试\n3. 退出\n请选择(1-3): ")

    if choice == "1":
        print("\n运行完整单元测试...")
        success = run_tests()
        exit_code = 0 if success else 1
        exit(exit_code)

    elif choice == "2":
        print("\n运行快速测试...")
        success = quick_test()
        exit_code = 0 if success else 1
        exit(exit_code)

    else:
        print("退出测试")
        exit(0)