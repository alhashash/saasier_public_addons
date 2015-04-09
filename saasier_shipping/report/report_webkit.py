import time
import locale
from report import report_sxw
from osv import osv
import urllib
import base64
from tools.translate import _
class report_webkit_html(report_sxw.rml_parse):
    
    _increment = 0
    _old_warehouse_id = 0
    _new_warehouse_id = 0
    
    def __init__(self, cr, uid, name, context):
        super(report_webkit_html, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'locale': locale,
            'cr':cr,
            'uid': uid,
            'get_label':self._get_label,
            'get_move_lines':self._get_move_lines,
            'get_move_count':self._get_move_count,
            
        })
        
        
    def _get_move_lines(self, picking_id, tracking_id):
         

        move_obj = self.pool.get('stock.move')
        move_ids = move_obj.search(self.cr,self.uid,[('picking_id','=',picking_id),('tracking_id','=',tracking_id)])

        if self._increment == 1:    
            if self._new_warehouse_id == self._old_warehouse_id:
                print 'warehouse same'
            else:
                raise osv.except_osv(_('Message!'),  _('Same Warehouse are not there, can not merge pdf !!'))
        self._old_warehouse_id = self._new_warehouse_id
        self._increment = 1     

            
        return move_obj.browse(self.cr,self.uid,move_ids)
#    
    def _get_move_count(self, picking):
        l = len(picking.move_lines)
        print "======***************==============>",l
        print "===========range(1,16-l)===========>",range(1,16-l)
        return range(1,16-l)
    
    def _get_label(self, picking_id):
        
        ###### used for warehouse domain added by 4devnet #####
        self.cr.execute("""select location_id from stock_move where picking_id=%s""",(picking_id.id,))
        loc_id = self.cr.fetchall()
        self._new_warehouse_id = loc_id[0][0]
     
        
        print "====picking_id======>",picking_id
        attach_obj = self.pool.get('ir.attachment')
        attach_ids = attach_obj.search(self.cr,self.uid,[('res_model','=','stock.picking.out'),('res_id','=',picking_id.id)])
        print "attach_ids: ",attach_ids

        if attach_ids:
            attach_obj.browse(self.cr,self.uid,attach_ids[0]).url
#           print "label: ",label
            return attach_obj.browse(self.cr,self.uid,attach_ids)
        return False

        
        
report_sxw.report_sxw('report.webkit.html',
                       'stock.picking.out',
                       'shipping_postmaster/report/report_webkit.mako',
                       parser=report_webkit_html,
                       )
