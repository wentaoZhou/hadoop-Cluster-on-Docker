CREATE TABLE `tenant` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `label` int(16) NOT NULL COMMENT '资源种类标识',
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  `finish_at` datetime DEFAULT NULL COMMENT '失效时间',
  `users_id` varchar(32) NOT NULL,
  `status` varchar(32) DEFAULT 'notRunning' COMMENT 'running   notRunning',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

CREATE TABLE `userstenant` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `tenant_id` int(32) NOT NULL COMMENT '租户id',
  `users_id` varchar(32) NOT NULL COMMENT '用户id',
  `permissions_id` int(32) NOT NULL COMMENT '权限id',
  `creator` varchar(32) NOT NULL COMMENT '授权者',
  `create_at` datetime DEFAULT NULL,
  `update_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;


CREATE TABLE `users` (
  `id` int(32) NOT NULL AUTO_INCREMENT COMMENT '用户id',
  `name` varchar(32) NOT NULL COMMENT '用户名',
  `password` varchar(127) NOT NULL COMMENT '用户密码',
  `phone` varchar(32) DEFAULT NULL COMMENT '电话号码',
  `email` varchar(32) DEFAULT NULL COMMENT '邮箱',
  `update_at` datetime DEFAULT NULL COMMENT '更新时间',
  `create_at` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;



CREATE TABLE `tenantstatus` (
  `id` int(32) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `container` varchar(32) NOT NULL COMMENT '节点名',
  `raw` varchar(127) NOT NULL COMMENT '内存使用',
  `percent` varchar(32) DEFAULT NULL COMMENT '存储使用占比',
  `cpu` varchar(32) DEFAULT NULL COMMENT 'CPU使用率',
  `networkIO` varchar(32) DEFAULT NULL COMMENT '网络速度',
  `BlockIO` varchar(32) DEFAULT NULL COMMENT '硬盘io',
  `update_at` datetime DEFAULT NULL COMMENT '更新时间',
  `create_at` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;


CREATE TABLE `permissions` (
  `id` int(32) NOT NULL,
  `add_member` int(2) NOT NULL DEFAULT '0' COMMENT '0-无权限   1-有权限',
  `delete_member` int(2) NOT NULL DEFAULT '0' COMMENT '0-无权限   1-有权限',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;