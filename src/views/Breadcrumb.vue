<template>
    <div class="example-container">
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item v-for="(item, index) in breadList" :key="index"
                :to="{ path: item.path }">{{ item.meta.title }}</el-breadcrumb-item>
        </el-breadcrumb>
    </div>
</template>
<script>
export default {
    props: {
        menuTree: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            breadList: [] // 路由集合
        };
    },
    watch: {
        $route() {
            this.getBreadcrumb();
        }
    },
    methods: {
        isHome(route) {
            return route.name === "Home"; //返回布尔值
        },
        getBreadcrumb() {
            const menuTree = this.menuTree;
            const currentRoute = this.$route;  
            // 初始化面包屑列表
            let breadcrumbList = [];
            
            // 如果当前路由不是首页，添加首页到面包屑
            if (!this.isHome(this.$route)) {
                breadcrumbList.push({ path: "/Hinfo", meta: { title: "首页" } });
            }
            
            // 递归查找当前路由对应的菜单路径
            const findMenuPath = (menus, currentPath, path = []) => {
                for (const menu of menus) {
                    const fullPath = [...path, menu].map(item => item.menuClick).join('/');
                    const menuPath = `/${fullPath}`;
                    // 处理根路径情况
                    if (currentPath === '/' && menuPath === '/') {
                        return [...path, menu];
                    }
                    // 比较完整路径
                    if (currentPath === menuPath) {
                        return [...path, menu];
                    }
                    if (currentPath.startsWith(menuPath + '/') && menu.children) {
                        const childPath = findMenuPath(menu.children, currentPath, [...path, menu]);
                        if (childPath) {
                            return childPath;
                        }
                    }
                }
                return null;
            };
            
            const currentPath = currentRoute.path;
            const menuPath = findMenuPath(menuTree, currentPath);
            
            if (menuPath) {
                for (const menu of menuPath) {
                    const fullPath = menuPath.slice(0, menuPath.indexOf(menu) + 1).map(item => item.menuClick).join('/');
                    breadcrumbList.push({
                        path: `/${fullPath}`,
                        meta: { title: menu.menuName }
                    });
                }
            }
            
            this.breadList = breadcrumbList;
        }
    },
    created() {
        this.getBreadcrumb();
    }
};
</script>
<style>
    .example-container {
        padding: 5px;
        background-color: #f5f7fa;
        border-radius: 4px;
        margin-bottom: 5px;
    }

    .el-breadcrumb {
        font-size: 5px;
        color: #606266;
    }

    .el-breadcrumb__item:last-child .el-breadcrumb__inner,
    .el-breadcrumb__item:last-child .el-breadcrumb__inner a,
    .el-breadcrumb__item:last-child .el-breadcrumb__inner a:hover,
    .el-breadcrumb__item:last-child .el-breadcrumb__inner:hover {
        color: #409eff;
        font-weight: bold;
    }

    .el-breadcrumb__inner,
    .el-breadcrumb__inner a {
        color: #606266;
        text-decoration: none;
    }

    .el-breadcrumb__inner a:hover,
    .el-breadcrumb__inner:hover {
        color: #409eff;
        cursor: pointer;
    }

    .el-breadcrumb__separator {
        margin: 0 5px;
        color: #c0c4cc;
    }
</style>
