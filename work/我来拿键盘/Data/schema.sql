CREATE DATABASE IF NOT EXISTS `fzu_history` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `fzu_history`;

CREATE TABLE IF NOT EXISTS `account_limit` (
  `id` INT PRIMARY KEY,
  `college_min` TINYINT NOT NULL,
  `college_max` TINYINT NOT NULL,
  `year_min` TINYINT NOT NULL,
  `year_max` TINYINT NOT NULL,
  `major_min` TINYINT NOT NULL,
  `major_max` TINYINT NOT NULL,
  `class_min` TINYINT NOT NULL,
  `class_max` TINYINT NOT NULL,
  `student_min` TINYINT NOT NULL,
  `student_max` TINYINT NOT NULL,
  `require_digit` TINYINT(1) NOT NULL,
  `require_lower` TINYINT(1) NOT NULL,
  `require_upper` TINYINT(1) NOT NULL,
  `require_special` TINYINT(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `users` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `student_id` CHAR(9) NOT NULL UNIQUE,
  `name` VARCHAR(255) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `avatars` (
  `id` INT PRIMARY KEY AUTO_INCREMENT,
  `path` VARCHAR(512) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `user_settings` (
  `user_id` BIGINT PRIMARY KEY,
  `avatar_id` INT NULL,
  `avatar_path` VARCHAR(512) NULL,
  `updated_at` DATETIME NOT NULL,
  CONSTRAINT `fk_user_settings_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
  CONSTRAINT `fk_user_settings_avatar` FOREIGN KEY (`avatar_id`) REFERENCES `avatars`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `avatars` (`id`, `path`) VALUES (1, '/static/avatar/default1.png')
ON DUPLICATE KEY UPDATE `id`=`id`;

INSERT INTO `account_limit` (
  `id`, `college_min`, `college_max`, `year_min`, `year_max`, `major_min`, `major_max`, `class_min`, `class_max`, `student_min`, `student_max`,
  `require_digit`, `require_lower`, `require_upper`, `require_special`
) VALUES (1, 1, 99, 0, 99, 0, 5, 0, 9, 0, 99, 1, 0, 0, 0)
ON DUPLICATE KEY UPDATE `id`=`id`;

-- 创建打卡评论表
CREATE TABLE IF NOT EXISTS `checkin_comments` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `location_id` INT NOT NULL,
  `user_id` BIGINT NOT NULL,
  `content` TEXT NOT NULL,
  `image_url` VARCHAR(512) NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_checkin_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建索引以提高查询性能
CREATE INDEX `idx_checkin_location` ON `checkin_comments`(`location_id`);
CREATE INDEX `idx_checkin_created` ON `checkin_comments`(`created_at`);

-- 创建学院评论表
CREATE TABLE IF NOT EXISTS `college_comments` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `college_id` INT NOT NULL,
  `user_id` BIGINT NOT NULL,
  `parent_id` BIGINT NULL,  -- NULL表示顶级评论，否则是回复
  `content` TEXT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT `fk_college_comment_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_college_comment_parent` FOREIGN KEY (`parent_id`) REFERENCES `college_comments`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建学院评论点赞表
CREATE TABLE IF NOT EXISTS `college_comment_likes` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `comment_id` BIGINT NOT NULL,
  `user_id` BIGINT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY `unique_like` (`comment_id`, `user_id`),
  CONSTRAINT `fk_comment_like_comment` FOREIGN KEY (`comment_id`) REFERENCES `college_comments`(`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_comment_like_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建索引以提高查询性能
CREATE INDEX `idx_college_comment_college` ON `college_comments`(`college_id`);
CREATE INDEX `idx_college_comment_parent` ON `college_comments`(`parent_id`);
CREATE INDEX `idx_college_comment_created` ON `college_comments`(`created_at`);
CREATE INDEX `idx_comment_like_comment` ON `college_comment_likes`(`comment_id`);

-- 合成大西瓜分数表
CREATE TABLE IF NOT EXISTS `watermelon_scores` (
  `id` BIGINT PRIMARY KEY AUTO_INCREMENT,
  `user_id` BIGINT NULL,
  `score` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_score` (`score`),
  INDEX `idx_user` (`user_id`),
  INDEX `idx_created` (`created_at`),
  CONSTRAINT `fk_watermelon_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
