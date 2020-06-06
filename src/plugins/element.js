import Vue from 'vue'
import { Button, Form, FormItem, Input, Message, Container, Header, Aside, Main, Menu, Submenu,
         MenuItem, Breadcrumb, BreadcrumbItem, Popover, Card, Row, Col, Table, TableColumn,
        Tooltip, Pagination, Dialog, DatePicker, Select, Option, MessageBox, Loading, Collapse, Tag,
    Dropdown, DropdownItem, DropdownMenu, Tabs, TabPane, Backtop
} from 'element-ui'

Vue.use(Button)
Vue.use(Form)
Vue.use(FormItem)
Vue.use(Input)
Vue.use(Container)
Vue.use(Header)
Vue.use(Aside)
Vue.use(Main)
Vue.use(Menu)
Vue.use(MenuItem)
Vue.use(Submenu)
Vue.use(Breadcrumb)
Vue.use(BreadcrumbItem)
Vue.use(Popover)
Vue.use(Card)
Vue.use(Row)
Vue.use(Col)
Vue.use(Table)
Vue.use(TableColumn)
Vue.use(Tooltip)
Vue.use(Pagination)
Vue.use(Dialog)
Vue.use(DatePicker)
Vue.use(Select)
Vue.use(Option)
Vue.use(Loading)
Vue.use(Collapse)
Vue.use(Tag)
Vue.use(Dropdown)
Vue.use(DropdownMenu)
Vue.use(DropdownItem)
Vue.use(Tabs)
Vue.use(TabPane)
Vue.use(Backtop)

Vue.prototype.$message = Message
Vue.prototype.$confirm = MessageBox.confirm
